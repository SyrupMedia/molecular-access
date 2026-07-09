#!/usr/bin/env bash

set -euxo pipefail

black apps
uncrustify --no-backup -c uncrustify.cfg core/src/*.cpp core/include/*.hpp core/src/bindings/*.{cpp,hpp}
shfmt --write misc/integration/tasks/*.sh tests/python/*.sh
