#!/usr/bin/env bash

set -euxo pipefail

echo "Running tests..."

molaccessd &

molmessg ./misc/integration/tasks/tests.molmsg