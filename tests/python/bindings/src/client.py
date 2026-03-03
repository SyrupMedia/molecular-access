import sys

from molecular_test_common import *

if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy

def on_update(data):
    print(f":: Called Python callback function.\n:: Client received the following: '{data}'")

if __name__ == "__main__":
    ipc_instance = molaccesspy.ManagedConsumer("molaccess-ipc-route-test")
    ipc_instance.subscribe_update(on_update)
