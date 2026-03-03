import sys

from molecular_test_common import *

if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy

if __name__ == "__main__":
    ipc_instance = molaccesspy.ManagedProducer("molaccess-ipc-route-test")
    ipc_instance.send_data("meow")
