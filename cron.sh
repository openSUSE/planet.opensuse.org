#!/bin/bash
set -e
basedir="${0%/*}"
[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

[ -e ./NOCRON ] && exit 0

LOGFILE="$PWD/website/log.txt"

{
    echo -n "START: "
    /bin/date -R
    ./update.sh
    ./write.sh
    echo -n "END: "
    /bin/date -R
} >"$LOGFILE" 2>&1
