#!/bin/bash

pushd website/images
for d in $(seq -w 1 31); do
    echo $d
    sed "s|@@|${d}|g" <day-template.svg | rsvg-convert --width=40 --height=40 --keep-aspect-ratio --format=png > "day-${d}.png"
done
