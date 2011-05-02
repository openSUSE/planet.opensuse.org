#!/bin/bash
set -e
basedir="${0%/*}"
[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

[ -e ./NOCRON ] && exit 0

LOGFILE="$PWD/website/log.txt"

{
    ./update.sh
    ./write.sh
} >"$LOGFILE" 2>&1
