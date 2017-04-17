#!/bin/bash

set -e

basedir="${0%/*}"
if [ $# -gt 0 ]; then
    for f in "$@"; do
        case $f in
            --*) ;;
            ?*)  eval "render_$f=1" ;;
        esac
    done
else
    render_all=1
fi

[ -n "$basedir" -a "$basedir" != "." ] && cd "$basedir"

function info { [ -n "$VERBOSE" ] && echo "INFO: $*" || :; }

if [ -n "$render_all" -o -n "$render_global" ]; then
    info "* global"
    mkdir -p website/global
    LC_ALL=en_US.utf8 \
    TZ=UTC \
    ./rawdog -d planetsuse/ \
        --output-dir=website/global \
        --write
fi

for lc in en_US de_DE es_ES pl_PL pt_PT ja_JP id_ID ru_RU cs_CZ zh_TW=tw ro_RO fr_FR hu_HU el_GR=gr mn_MN my_MM; do
    case $lc in
        *=*) lang="${lc##*=}"; lc="${lc%=*}" ;;
        *_*) lang="${lc%%_*}" ;;
    esac
    render_this="render_$lang"
    render="${!render_this}"
    [ -n "$render_all" -o -n "$render" ] || continue
    info "* $lang"
    mkdir -p website/"$lang"
    case $lc in
        *.*) lcu="$lc" ;;
        *) lcu="${lc}.utf8" ;;
    esac
    LC_ALL="$lcu" \
    TZ=UTC \
    ./rawdog -d planetsuse/ \
        --lang="$lang" \
        --locale="$lc" \
        --output-dir=website/"$lang" \
        --write
done
