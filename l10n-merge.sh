#!/bin/bash
set -e

pot=$(/bin/ls -1 ./locale/*.pot 2>/dev/null)
[ -n "$pot" ] || { echo "ERROR: failed to find .pot file in $PWD/locale" >&2; exit 1; }

for f in ./locale/*.po; do
    echo -n "${f}: "
    msgmerge --update "$f" "$pot"
done
