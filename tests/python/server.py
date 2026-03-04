"""
This is a test script which declares a Molecular IPC instance, and sends data
to another Molecular IPC instance function. This file should not be imported
as a module, nor distributed to end-users.
"""

import sys

from molecular_test_common import *

# This is bad practice, we are doing this to make testing easier.
# Do not ship something like this!
if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy

if __name__ == "__main__":
    ipc_instance = molaccesspy.ManagedProducer("molaccess-ipc-route-test")
    ipc_instance.send_data("meow")
