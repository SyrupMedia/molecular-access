#!/usr/bin/env sh

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

python3 "$SCRIPTPATH/molaccessd_test.py" &
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND CREATE Meow'
