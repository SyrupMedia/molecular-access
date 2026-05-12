#!/usr/bin/env bash

set -euxo pipefail

SOURCE_ROOT="$PWD"
INSTALL_DIRECTORY="$SOURCE_ROOT/installdir"
CONTAINER_DIRECTORY="misc/containers/$1"

if [ ! -d "$CONTAINER_DIRECTORY" ]; then
	exit 1
fi

mkdir "$INSTALL_DIRECTORY"

cd "$CONTAINER_DIRECTORY"
docker compose up --build --force-recreate

cd "$SOURCE_ROOT"

if [ -z "$(ls -A "$INSTALL_DIRECTORY")" ]; then
	echo ":: $INSTALL_DIRECTORY is empty!"
	exit 1
fi
