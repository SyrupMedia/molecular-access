#!/usr/bin/env bash

cmake --preset release
clang-tidy --fix -p=target/release/ core/include/*.hpp core/src/*.cpp core/src/bindings/*.{hpp,cpp}
