#!/usr/bin/env sh

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

python3 "$SCRIPTPATH/molaccessd_test.py" &
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND CREATE resource_name=Name resource_value=Value resource_value_default=DefaultValue resource_value_type=string'
