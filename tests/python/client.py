"""
This is a test script which declares a Molecular IPC instance, receives data
from another Molecular IPC instance, and passes that data to a callback
function. This file should not be imported as a module, nor distributed to
end-users.
"""

import sys

from molecular_test_common import *

# This is bad practice, we are doing this to make testing easier.
# Do not ship something like this!
if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy


def on_update(data: str):
    """
    A simple callback function which formats and prints a string passed to it
    from the ManagedConsumer object.
    """

    print(
        f":: Called Python callback function.\n:: Client received the following: '{data}'"
    )


if __name__ == "__main__":
    ipc_instance = molaccesspy.ManagedConsumer("molaccess-ipc-route-test")
    ipc_instance.subscribe_update(on_update)
