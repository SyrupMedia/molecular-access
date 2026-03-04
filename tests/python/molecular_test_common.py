"""
Common utility functions, data, and the likes for the testing scripts. This
module should not be used for anything other than such test scripts, and not
deployed to users.
"""

import os
import sys

from pathlib import PureWindowsPath


class TestData:
    """
    Contains data common to the testing scripts. Please do not create new
    objects from this class.
    """

    script_directory = os.path.dirname(os.path.realpath(__file__))
    script_directory = PureWindowsPath(
        os.path.normpath(PureWindowsPath(script_directory).as_posix())
    ).as_posix()

    depth_traversal_string: str = f"../.."
    installdir_root: str = f"{script_directory}/{depth_traversal_string}/installdir"
    libdirectory_unix: str = "usr/local/lib"

    common_distributions: list[str] = [
        "arch"
        "centos"
        "debian"
        "fedora"
        "gentoo"
        "mint"
        "nixos"
        "opensuse"
        "popos"
        "ubuntu"
        "void"
    ]

    search_directories: dict[str, str] = {
        "install_directory_linux_generic": f"{installdir_root}/{libdirectory_unix}",
        "install_directory_linux_root": f"/lib",
        "install_directory_linux_root_local": f"/{libdirectory_unix}",
        "install_directory_windows": f"{installdir_root}/Program Files (x86)/molecular-access/lib",
    }


def append_distribution_directories() -> dict[str, str]:
    """
    Iterate through the distributions, and append them as key-value pairs to the search dictionary.
    """

    new_search_directories = TestData.search_directories

    for distribution in TestData.common_distributions:
        new_search_directories[f"install_directory_linux_{distribution}"] = (
            f"{TestData.installdir_root}/{distribution}/{TestData.libdirectory_unix}"
        )

    TestData.search_directories = new_search_directories

    return new_search_directories


def append_import_directory() -> bool:
    """
    This is a function which searches for the existence of a valid Molecular
    library binary, and imports it as a Python module. You should not ship code
    which programatically imports Python modules. We are doing this solely to
    import modules which are not adequately packaged. Do not replicate.
    """

    found_directory: bool = False

    search_directories: dict[str, str] = append_distribution_directories()

    for search_directory in search_directories:
        directory = search_directories[search_directory]

        if os.path.exists(directory):
            print(f":: Found {directory}")

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
            # Optionally force `found_directory` on in case there is a valid module target.

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
