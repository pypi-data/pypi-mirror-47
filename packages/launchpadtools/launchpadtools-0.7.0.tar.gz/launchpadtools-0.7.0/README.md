Launchpad tools
===============

[![Build Status](https://travis-ci.org/nschloe/launchpadtools.svg?branch=master)](https://travis-ci.org/nschloe/launchpadtools)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/launchpadtools.svg)](https://codecov.io/gh/nschloe/launchpadtools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi Version](https://img.shields.io/pypi/v/launchpadtools.svg)](https://pypi.python.org/pypi/launchpadtools)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/launchpadtools.svg?logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/launchpadtools)

Some tools for easy submission to launchpad.

### Usage

All options are documented under `launchpad-submit -h`.

Sometimes, you may want to submit a source package with a Debian configuration that is
available somewhere else. This may help setting up a nightly submission process. As an
example, take the nightly submission script for a [Mixxx
PPA](https://launchpad.net/~nschloe/+archive/ubuntu/mixxx-nightly).

```
#!/bin/sh -ue

TMP_DIR=$(mktemp -d)
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

CACHE="$HOME/.cache/repo/mixxx"
git -C "$CACHE" pull || git clone "https://github.com/mixxxdj/mixxx.git" "$CACHE"
git clone --shared "$CACHE" "$TMP_DIR"

VERSION=$(grep "define MIXXX_VERSION" "$TMP_DIR/src/defs_version.h" | sed "s/[^0-9]*\([0-9][\.0-9]*\).*/\1/")
FULL_VERSION="$VERSION~$(date +"%Y%m%d%H%M%S")"

CACHE="$HOME/.cache/repo/mixxx-debian"
git -C "$CACHE" pull || git clone "git://anonscm.debian.org/git/pkg-multimedia/mixxx.git" "$CACHE"
rsync -a "$CACHE/debian" "$TMP_DIR"

launchpad-submit \
  --directory "$TMP_DIR" \
  --ubuntu-releases trusty xenial yakkety zesty \
  --ppa nschloe/mixxx-nightly \
  --version-override "$FULL_VERSION" \
  --version-append-hash \
  --update-patches
```

### Installation

The launchpad tools are [available from the Python Package
Index](https://pypi.python.org/pypi/launchpadtools/), so for installation/upgrading
simply do
```
pip3 install launchpadtools --user
```

### License

The launchpadtools are published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
