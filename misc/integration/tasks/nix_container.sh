#!/usr/bin/env bash

set -euxo pipefail

echo "Running tests..."

molaccessd &

molmessg /opt/tests.molmsg
