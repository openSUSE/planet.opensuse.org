#!/bin/bash
set -e
basedir="${0%/*}"
[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

./update.sh &>log
./write.sh &>>log
