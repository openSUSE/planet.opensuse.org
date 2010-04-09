#!/bin/bash
mo=$(/bin/ls -1 ./locale/*.pot)
mo="${mo##*/}"
mo="${mo%.*}"

for f in ./locale/*.po; do
    l="${f%.po}"
    l="${l##*/}"
    mkdir -p "./locale/$l/LC_MESSAGES"
    msgfmt -o "./locale/$l/LC_MESSAGES/$mo.mo" "$f"
done
