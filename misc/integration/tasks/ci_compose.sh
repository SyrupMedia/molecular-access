#!/usr/bin/env sh

set -e

DIRECTORY="misc/containers/$1"

if [ ! -d "$DIRECTORY" ]; then
    exit 1
fi

mkdir installdir
cd "$DIRECTORY"
docker compose up --build --force-recreate

if [ -z "$(ls -A "$DIRECTORY")" ]; then
	exit 1
fi
