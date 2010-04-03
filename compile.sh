#!/bin/bash
for d in \
libs/*/python*/site-packages/ \
rawdoglib \
planetsuse/plugins \
; do
    python -c "import compileall; compileall.compile_dir('${d}', force=1);"
done
