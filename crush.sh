#!/bin/bash

WD=
function on_exit { [ -n "$WD" ] && /bin/rm -rf "$WD"; }
WD=$(mktemp -d "/tmp/planet-opensuse-crush.XXXXXXXX")

for d in website/images website/hackergotchi; do
    pngcrush -q -d "$WD/" "$d"/*.png
    for f in "$WD"/*.png; do
        [ -e "$f" ] || continue
        size_crushed=$(stat -c '%s' "$f")
        size_orig=$(stat -c '%s' "$d/${f##*/}")
        if [ "$size_crushed" -lt "$size_orig" ]; then
            /bin/mv -v "$f" "$d/${f##*/}"
        else
            /bin/rm "$f"
        fi
    done
done
