#!/bin/bash
set -e

mo=$(/bin/ls -1 ./locale/*.pot)
mo="${mo##*/}"
mo="${mo%.*}"

for f in ./locale/*.po; do
    echo -n "$f: "
    l="${f%.po}"
    l="${l##*/}"
    mkdir -p "./locale/$l/LC_MESSAGES"
    msgfmt -o "./locale/$l/LC_MESSAGES/$mo.mo" "$f"
    echo "ok"
done
