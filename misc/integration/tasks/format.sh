#!/usr/bin/env bash

black apps
uncrustify --no-backup -c uncrustify.cfg core/src/*.cpp core/include/*.hpp core/src/bindings/*.{cpp,hpp}
