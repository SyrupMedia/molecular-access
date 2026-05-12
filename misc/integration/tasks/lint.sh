#!/usr/bin/env bash

pylint apps
pylint_result=$?

cmake --preset release
clang-tidy --warnings-as-errors="*" -p=target/release/ core/include/*.hpp core/src/*.cpp core/src/bindings/*.{hpp,cpp}
clangtidy_result=$?

exit $(($pylint_result || clangtidy_result))
