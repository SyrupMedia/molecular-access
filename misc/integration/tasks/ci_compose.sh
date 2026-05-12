#!/usr/bin/env bash

set -euxo pipefail

SOURCE_ROOT="$PWD"
CONTAINER_DIRECTORY="misc/containers/$1"

if [ ! -d "$CONTAINER_DIRECTORY" ]; then
	exit 1
fi

mkdir installdir

cd "$CONTAINER_DIRECTORY"
docker compose up --build --force-recreate

cd "$SOURCE_ROOT"

if [ -z "$(ls -A "$CONTAINER_DIRECTORY")" ]; then
	exit 1
fi
