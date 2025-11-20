import os
import sys

from pathlib import PureWindowsPath

script_directory = os.path.dirname(os.path.realpath(__file__))
script_directory = PureWindowsPath(
    os.path.normpath(PureWindowsPath(script_directory).as_posix())
).as_posix()

search_directories = {
    "install_directory_windows": f"{script_directory}/../../../installdir/Program Files (x86)/molecular-access/lib",
    "install_directory_linux": f"{script_directory}/../../../installdir/usr/local/lib",
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

    return found_directory


if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy

if __name__ == "__main__":
    molaccesspy.molecular_say_hello()
