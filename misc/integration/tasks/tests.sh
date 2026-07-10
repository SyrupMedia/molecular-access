#!/usr/bin/env bash

set -euxo pipefail

make
make install

cd ./tests/python/

exec ./run_bindings_test.sh
exec ./run_message_test.sh
