#!/bin/bash

basedir="${0%/*}"

[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

./rawdog -d planetsuse/ --write
