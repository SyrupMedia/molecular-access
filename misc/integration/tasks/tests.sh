#!/usr/bin/env bash

make
make install
cd ./tests/python/
exec ./run_bindings_test.sh
