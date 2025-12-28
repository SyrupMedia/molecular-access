import os
import sys
import threading

from pathlib import PureWindowsPath

script_directory = os.path.dirname(os.path.realpath(__file__))
script_directory = PureWindowsPath(
    os.path.normpath(PureWindowsPath(script_directory).as_posix())
).as_posix()

search_directories = {
    "install_directory_windows": f"{script_directory}/../../../installdir/Program Files (x86)/molecular-access/lib",
    "install_directory_linux": f"{script_directory}/../../../installdir/usr/local/lib",
    "install_directory_linux": f"{script_directory}/../../../installdir/ubuntu/usr/local/lib",
    "install_directory_linux": f"{script_directory}/../../../installdir/fedora/usr/local/lib",
}


def append_import_directory() -> bool:
    found_directory: bool = False

    for search_directory in search_directories:
        directory = search_directories[search_directory]

        if os.path.exists(directory):
            if os.path.exists(f"{directory}/_molaccesspy.so") or os.path.exists(
                f"{directory}/_molaccesspy.pyd"
            ):
                if os.path.exists(f"{directory}/molaccesspy.py"):
                    sys.path.append(directory)

                    print(f":: Using {directory}")

                    found_directory = True

                    break

    if not found_directory:
        print(":: Found no suitable instance of the molaccesspy module.")
        while True:
            message_input = input(":: Continue trying import? Yes/No\n").lower()

            match message_input:
                case "yes":
                    found_directory = True
                    break
                case "y":
                    found_directory = True
                    break
                case "no":
                    found_directory = False
                    break
                case "n":
                    found_directory = False
                    break

    return found_directory


if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy

def listen():
    def on_update():
        print("Updating!")
    
    print("Runing listener.")
    
    molecular_ipc_instance = molaccesspy.molecular_ipc_listener_create("molaccess-ipc-route-test2")
    molaccesspy.molecular_ipc_listener_update(molecular_ipc_instance, on_update)

def produce():
    print("Runing producer.")

    molecular_ipc_instance = molaccesspy.molecular_ipc_producer_create("molaccess-ipc-route-test2")

    molaccesspy.molecular_ipc_producer_wait_for_listener(molecular_ipc_instance)

    molaccesspy.molecular_send(molecular_ipc_instance, "Meow")

if __name__ == "__main__":
    molaccesspy.molecular_say_hello() 

    thread_listener = threading.Thread(target=listen)
    thread_producer = threading.Thread(target=produce)

    thread_listener.start()
    thread_producer.start()

    thread_listener.join()
    thread_producer.join()


    