#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatically create tarball and submit it to launchpad.
"""
import argparse
import launchpadtools


def _parse_cmd_arguments():
    parser = argparse.ArgumentParser(description="Submit builds to launchpad.")
    parser.add_argument(
        "-d",
        "--directory",
        required=True,
        help="Directory to submit. Must contain sources and ./debian`.",
    )
    parser.add_argument(
        "-u",
        "--ubuntu-releases",
        help="Ubuntu releases to build for",
        required=True,
        nargs="+",
    )
    parser.add_argument("-p", "--ppa", help="PPA to submit to", type=str, required=True)
    parser.add_argument(
        "-l",
        "--launchpad-login",
        help="login name on launchpad (for SFTP)",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o", "--version-override", help="Override package version", type=str
    )
    parser.add_argument(
        "-t",
        "--version-append-datetime",
        help="Append date/time to version (useful for avoiding upload rejection from launchpad)",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-a",
        "--version-append-hash",
        help="Append code hash to version (useful for deduplication)",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--update-patches",
        help="Automatically update patches",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Force submission even if build is already uploaded",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-b",
        "--debuild-params",
        help="extra parameters passed to debuild",
        type=str,
        default="",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="launchpadtools %s" % launchpadtools.__version__,
    )
    return parser.parse_args()


def main():
    args = _parse_cmd_arguments()
    launchpadtools.submit.submit(
        args.directory,
        args.ubuntu_releases,
        args.ppa,
        args.launchpad_login,
        args.debuild_params,
        args.version_override,
        args.version_append_datetime,
        args.version_append_hash,
        args.force,
        args.update_patches,
    )
    return
