import sys
import threading

from molecular_test_common import *

# This is bad practice, we are doing this to make testing easier.
# Do not ship something like this!
if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy


def thread_main():
    ipc_instance = molaccesspy.ManagedProducer("molaccessd")
    ipc_instance.send_data("meow")


if __name__ == "__main__":
    thread = threading.Thread(target=thread_main)
    thread.start()
    thread.join()
