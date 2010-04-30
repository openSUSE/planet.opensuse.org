#!/bin/bash
set -e
basedir="${0%/*}"
[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

[ -e ./NOCRON ] && exit 0

./update.sh >log 2>&1
./write.sh >>log 2>&1
