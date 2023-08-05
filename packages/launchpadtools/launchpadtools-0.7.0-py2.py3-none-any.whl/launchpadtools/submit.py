# -*- coding: utf-8 -*-
#
from __future__ import print_function

from distutils.dir_util import copy_tree
import os
import re
import shutil
import subprocess
import time
import tempfile

import git
from launchpadlib.launchpad import Launchpad


class DputException(Exception):
    pass


def _get_info_from_changelog(changelog):
    with open(changelog, "r") as handle:
        first_line = handle.readline()
    search = re.search("^( *[^ ]+) *\\(([^\\)]+)\\).*", first_line, re.IGNORECASE)
    assert search, "Could not extract name from changelog."
    return search.group(1), search.group(2)


def _parse_package_version(version):
    """Dissect version in upstream, debian/ubuntu parts.
    """
    out = re.match("(([0-9]+):)?(.*)", version)
    if out:
        epoch = out.group(2)
        version = out.group(3)
    else:
        epoch = None

    parts = version.split("-")
    out = re.match("([0-9\\.]*)[a-z]*([0-9\\.]*)", parts[-1])
    if len(parts) > 1 and out:
        upstream = "-".join(parts[:-1])
        debian = out.group(1)
        ubuntu = out.group(2)
    else:
        upstream = version
        debian = None
        ubuntu = None

    return epoch, upstream, debian, ubuntu


def _get_tree_hash(directory):
    """Returns Git tree hash of a directory.
    """
    try:
        repo = git.Repo(directory)
    except git.InvalidGitRepositoryError:
        repo = git.Repo.init(directory)

    # The add step can take really long if many files need to be added.  Use git's own
    # `git add -A` rather than GitPython's repo.index.add('*') since the latter takes a
    # really long time if the repo is large, even if it's already almost completely
    # checked in.
    repo.git.add("-A")
    repo.index.commit("launchpadtools commit")
    tree_hash = repo.tree().hexsha

    # clean up
    shutil.rmtree(os.path.join(directory, ".git"))

    return tree_hash


def _get_filesize(path):
    size_in_bytes = os.path.getsize(path)
    return _sizeof_fmt(size_in_bytes)


def _sizeof_fmt(num, suffix="B"):
    # <http://stackoverflow.com/a/1094933/353337>
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def _create_tarball(directory, tarball, prefix, excludes=None):
    if excludes is None:
        excludes = []

    assert not isinstance(excludes, str)

    if os.path.isfile(tarball):
        os.remove(tarball)
    # We need to make sure that the same content ends up with a tar archive that has the
    # same checksums. Unfortunately, by default, gzip contains time stamps. Stripping
    # them helps <http://serverfault.com/a/110244/132462>.
    # Also, replace the leading `repo_dir` by `prefix`.
    repo_dir_without_leading_slash = directory[1:] if directory[0] == "/" else directory
    transform = "s/^{}/{}/".format(
        repo_dir_without_leading_slash.replace("/", "\\/"), prefix
    )
    cmd = [
        "tar",
        "--transform",
        transform,
        "-czf",
        tarball,
        # "--use-compress-program",
        # "'gzip -n'",
    ]
    for exclude in excludes:
        cmd.append(f"--exclude={exclude}")
    cmd.append(directory)

    subprocess.check_call(cmd)
    return


def _release_has_same_hash(name, tree_hash_short, ppa, ubuntu_release):
    # Check if this version has already been published.
    published_in_series = ppa.getPublishedSources(
        source_name=name,
        status="Published",
        distro_series=(f"https://api.launchpad.net/1.0/ubuntu/{ubuntu_release}"),
    )

    has_same_hash = False
    # Expect a package version of the form
    # 2.1.0~20160504184836-01b3a567-trusty1
    if published_in_series.entries:
        # The source_package_versions have the form
        #
        #   4.3.1-developer~20161001024503-3ea99bea-1trusty1
        #
        # Split those at `-` and take the second-to-last, namely the hash.
        parts = published_in_series.entries[0]["source_package_version"].split("-")
        has_same_hash = len(parts) >= 3 and parts[-2] == tree_hash_short

    return has_same_hash


def submit(
    directory,
    ubuntu_releases,
    ppa_string,
    launchpad_login_name,
    debuild_params="",
    version_override=None,
    version_append_hash=False,
    force=False,
    do_update_patches=False,
    dry=False,
):
    assert os.path.isdir(os.path.join(directory, "debian")), "debian/ directory missing"

    # create temporary working directory
    with tempfile.TemporaryDirectory() as work_dir:
        orig_dir = os.path.join(work_dir, "orig")

        print("Copying directory...")
        tic = time.time()
        copy_tree(directory, orig_dir)
        # remove git folder
        shutil.rmtree(os.path.join(orig_dir, ".git"))
        debian_dir = os.path.join(orig_dir, "debian")
        assert os.path.isdir(debian_dir)
        elapsed_time = time.time() - tic
        print(f"done (took {elapsed_time:.1f}s).")

        name, version = _get_info_from_changelog(os.path.join(debian_dir, "changelog"))

        print("\nComputing tree hash...")
        tic = time.time()
        tree_hash_short = _get_tree_hash(orig_dir)[:8]
        elapsed_time = time.time() - tic
        print(f"done ({tree_hash_short}, took {elapsed_time:.1f}s).")

        # check which ubuntu series we need to submit to
        if force:
            submit_releases = ubuntu_releases
        else:
            # Check if this version has already been published.
            print("\nCheck for tree hash on PPA...")
            launchpad = Launchpad.login_anonymously("foo", "production", None)
            ppa_owner, ppa_name = tuple(ppa_string.split("/"))
            owner = launchpad.people[ppa_owner]
            ppa = owner.getPPAByName(name=ppa_name)

            submit_releases = [
                release
                for release in ubuntu_releases
                if not _release_has_same_hash(name, tree_hash_short, ppa, release)
            ]
            print("done.")

        if not submit_releases:
            print("\nEverything up-to-date. No submissions necessary.\n")
            return

        print("\nSubmitting to {}.\n".format(", ".join(submit_releases)))

        # Dissect version in upstream, debian/ubuntu parts.
        epoch, upstream_version, debian_version, ubuntu_version = _parse_package_version(
            version
        )

        if do_update_patches:
            _update_patches(orig_dir)

        if version_override:
            upstream_version = version_override
            debian_version = "1"
            ubuntu_version = "1"

        # Use the `-` as a separator (instead of `~` as it's often seen) to make sure that
        # ${UBUNTU_RELEASE}x isn't part of the name. This makes it possible to increment `x`
        # and have launchpad recognize it as a new version.
        if version_append_hash:
            upstream_version += f"-{tree_hash_short}"

        # Create orig tarball (without the Debian folder).
        orig_tarball = os.path.join(work_dir, f"{name}_{upstream_version}.orig.tar.gz")
        prefix = name + "-" + upstream_version
        print("Creating tarball...")
        tic = time.time()
        _create_tarball(orig_dir, orig_tarball, prefix, excludes=["./debian"])
        elapsed_time = time.time() - tic
        print(
            "done ({}, took {:.1f}s).\n".format(
                _get_filesize(orig_tarball), elapsed_time
            )
        )

        for ubuntu_release in submit_releases:
            try:
                _submit(
                    work_dir,
                    [orig_tarball],
                    orig_dir,
                    name,
                    upstream_version,
                    debian_version,
                    ubuntu_version,
                    ubuntu_release,
                    epoch,
                    ppa_string,
                    launchpad_login_name,
                    debuild_params,
                    dry,
                )
            except DputException:
                pass
    return


def _submit(
    work_dir,
    orig_tarballs,
    orig_dir,
    name,
    upstream_version,
    debian_version,
    ubuntu_version,
    ubuntu_release,
    slot,
    ppa_string,
    launchpad_login_name,
    debuild_params="",
    dry=False,
):
    # quick workaround
    # TODO fix
    assert len(orig_tarballs) == 1
    orig_tarball = orig_tarballs[0]

    # Assert tarball at
    #     /work_dir/trilinos_4.3.1.2~20121123-01b3a567.orig.tar.gz.
    #
    _, ext = os.path.splitext(orig_tarball)
    tarball_dest = f"{name}_{upstream_version}.orig.tar{ext}"
    assert os.path.isfile(os.path.join(work_dir, tarball_dest))

    # Get last component of `orig_dir`, cf.
    # <http://stackoverflow.com/a/3925147/353337>.
    prefix = os.path.basename(os.path.normpath(orig_dir))
    assert os.path.isdir(orig_dir)

    debian_dir = os.path.join(work_dir, prefix, "debian")
    assert os.path.isdir(debian_dir)

    # We cannot use "-ubuntu1" as a suffix here since we'd like to submit for multiple
    # ubuntu releases. If the version strings were exactly the same, the following error
    # is produced on upload:
    #
    #   File gmsh_2.12.1~20160512220459-ef262f68-ubuntu1.debian.tar.gz
    #   already exists in Gmsh nightly, but uploaded version has different
    #   contents.
    #
    chlog_version = upstream_version + "-"
    if debian_version:
        chlog_version += debian_version
    if ubuntu_version:
        chlog_version += ubuntu_release + ubuntu_version
    else:
        chlog_version += ubuntu_release + "1"

    slot_version = chlog_version
    if slot:
        slot_version = slot + ":" + chlog_version

    # From `man dpkg-genchanges`:
    # By default, or if specified, the original source will be included only if the
    # upstream version number (the version without epoch and without Debian revision)
    # differs from the upstream version number of the previous changelog entry.
    #
    # This means that, if this version and the last coincide, the source will not be
    # uploaded, leading to launchpad errors of the kind
    # ```
    # Unable to find matplotlib_2.0.0~beta4.orig.tar.gz in upload or distribution.
    # ```
    # Hence, remove old changelog and create it anew.
    os.remove(os.path.join(work_dir, prefix, "debian", "changelog"))
    subprocess.check_call(
        [
            "dch",
            "--create",
            "--package",
            name,
            # '-b',  # force
            "-v",
            slot_version,
            "--distribution",
            ubuntu_release,
            "launchpad-submit update",
        ],
        cwd=os.path.join(work_dir, prefix),
    )

    if dry:
        return

    # Call debuild, the actual workhorse
    subprocess.check_call(
        [
            "debuild",
            debuild_params,
            "-S",  # build source package only
            # build dependencies are only needed on launchpad, not locally
            "--no-check-builddeps",
            "--lintian-opts",
            "-EvIL",
            "+pedantic",
        ],
        cwd=os.path.join(work_dir, prefix),
    )

    # Submit to launchpad.
    print()
    print(f"Uploading to PPA {ppa_string}...")
    print()
    for filename in [
        # f"{name}_{chlog_version}.debian.tar.xz",
        f"{name}_{chlog_version}.dsc",
        f"{name}_{chlog_version}_source.build",
        f"{name}_{chlog_version}_source.changes",
        f"{name}_{upstream_version}.orig.tar.gz",
    ]:
        size_str = _get_filesize(os.path.join(work_dir, filename))
        print(f"    {filename}: {size_str}")
    print()

    # Alternative upload from Ubuntu:
    # ```
    # subprocess.check_call([
    #     "dput",
    #     f"ppa:{ppa_string}",
    #     f"{name}_{chlog_version}_source.changes"
    #     ])
    # ```
    # This does not take SFTP however.

    # Debian's dput must be told about the launchpad PPA via a config file. Make it
    # temporary.
    dput_config = os.path.join(work_dir, "dput.cf")
    # Try using SFTP here first; amongst other things, it's more robust against flaky
    # connections.
    # Note that launchpad must have a valid public key, and ppa.launchpad.net must have
    # been added to the list of known hosts.
    # See <https://unix.stackexchange.com/a/368141/40432>.
    configs = [("sftp", launchpad_login_name), ("ftp", "anonymous")]
    success = False
    for method, login_name in configs:
        with open(dput_config, "w") as f:
            f.write(
                f"""[{name}-nightly]
fqdn = ppa.launchpad.net
method = {method}
incoming = ~{ppa_string}/ubuntu/
login = {login_name}
allow_unsigned_uploads = 0"""
            )
        try:
            subprocess.check_call(
                [
                    "dput",
                    "-c",
                    dput_config,
                    f"{name}-nightly",
                    f"{name}_{chlog_version}_source.changes",
                ],
                os.chdir(work_dir),
            )
        except subprocess.CalledProcessError as exception:
            print("Command:")
            print(" ".join(exception.cmd))
            print("Return code:")
            print(exception.returncode)
            print("Output:")
            print(exception.output)
        else:
            success = True
            break

    if not success:
        raise DputException

    return


def _update_patches(directory):
    """debuild's patch apply doesn't allow fuzz, but fuzz is often what happens
    when applying a Debian patch to the master branch. `patch` itself is more
    robust, so use that here to update the Debian patches.
    """
    print("Updating patches...")

    # We need the number of patches so we don't call `quilt push` too often.
    out = subprocess.check_output(
        ["quilt", "series"], env={"QUILT_PATCHES": "debian/patches"}, cwd=directory
    )
    all_patches = out.decode("utf-8").split("\n")[:-1]

    for patch in all_patches:
        try:
            subprocess.check_call(
                ["quilt", "push"],
                env={"QUILT_PATCHES": "debian/patches"},
                cwd=directory,
            )
            subprocess.check_call(
                ["quilt", "refresh"],
                env={"QUILT_PATCHES": "debian/patches"},
                cwd=directory,
            )
        except subprocess.CalledProcessError:
            # If applied and refreshing the patch didn't work, remove it.
            print("Deleting patch {patch}...")
            subprocess.check_call(
                ["quilt", "delete", "-nr"],
                env={"QUILT_PATCHES": "debian/patches"},
                cwd=directory,
            )

    # undo all patches; only the changes in the debian/patches/ remain.
    out = subprocess.check_output(
        ["quilt", "series"], env={"QUILT_PATCHES": "debian/patches"}, cwd=directory
    )
    all_patches = out.decode("utf-8").split("\n")[:-1]
    if all_patches:
        subprocess.check_call(
            ["quilt", "pop", "-a"],
            env={"QUILT_PATCHES": "debian/patches"},
            cwd=directory,
        )

    # Remove the ubuntu.series file since it's not handled by quilt.
    ubuntu_series = os.path.join(directory, "debian", "patches", "ubuntu.series")
    if os.path.isfile(ubuntu_series):
        os.remove(ubuntu_series)
    return
