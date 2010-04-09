#!/bin/bash

basedir="${0%/*}"

[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

LC_ALL=en_US.utf8 \
./rawdog -d planetsuse/ --update
