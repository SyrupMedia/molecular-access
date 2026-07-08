#!/usr/bin/env sh

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

python3 "$SCRIPTPATH/molaccessd_test.py" &

# Announce to `molaccessd`
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND ANNOUNCE connection_route=announcetest3 resource_collection=Testing'

# Creation
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND CREATE resource_name=Name resource_value=Value resource_value_default=DefaultValue resource_value_type=string'

# Reading
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND STAT resource_name=Name'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND READ resource_name=Name'

# Writing
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND SET resource_name=Name resource_value=ValueSet'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UPDATE resource_name=Name resource_value=ValueUpdate'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND RESET resource_name=Name'

# Locking tests
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND LOCK resource_name=Name'

python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND SET resource_name=Name resource_value=ValueSetLockTest'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UPDATE resource_name=Name resource_value=ValueUpdateLockTest'

python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UNLOCK resource_name=Name'

python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND SET resource_name=Name resource_value=ValueSetUnlockTest'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UPDATE resource_name=Name resource_value=ValueUpdateUnlockTest'

python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND LOCK resource_name=Name'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND SET resource_name=Name resource_value=ValueSetLockTest2'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UNLOCK resource_name=Name'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND SET resource_name=Name resource_value=ValueSetUnlockTest2'

python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND LOCK resource_name=Name'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UPDATE resource_name=Name resource_value=ValueUpdateLockTest2'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UNLOCK resource_name=Name'
python3 "$SCRIPTPATH/molmessg_test.py" -c 'SEND UPDATE resource_name=Name resource_value=ValueUpdateUnlockTest2'