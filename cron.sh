#!/bin/bash
set -e
basedir="${0%/*}"
[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

[ -e ./NOCRON ] && exit 0
[ -e ./NOPULL ] || {
    git pull --quiet
}

LOGFILE="$PWD/website/log.txt"

{
    REV=$(git rev-parse HEAD)
    echo -n "========== START ($REV): "
    /bin/date -R
    ./update.sh 2>&1
    ./write.sh 2>&1
    echo -n "========== END ($REV): "
    /bin/date -R
} >"$LOGFILE" 2>&1
