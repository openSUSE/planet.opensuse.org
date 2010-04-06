#!/bin/bash

set -e

basedir="${0%/*}"

[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

./rawdog -d planetsuse/ \
    --lang "en" \
    --output-file ../website/index.html \
    --old-output-file ../website/old.html \
    --old-output-link old.html \
    --write

for lang in de es pl pt jp; do
    ./rawdog -d planetsuse/ \
        --lang "$lang" \
        --output-file ../website/"$lang".html \
        --old-output-file ../website/"$lang"-old.html \
        --old-output-link "$lang"-old.html \
        --no-feed-list \
        --write
done
