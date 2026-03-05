#!/usr/bin/env python3

"""
The entrypoint for the `molaccessd` process, meant to be run as an executable.
This file should not be imported as a module.
"""

import molaccesspy

from tinydb import TinyDB, Query


class MolecularResourceManager:
    database_instance = None

    resource_keys: list[str] = [
        "resource_collection",
        "resource_methods_allowed",
        "resource_methods_provided",
        "resource_name",
        "resource_state_callable",
        "resource_state_locked",
        "resource_time_creation",
        "resource_time_last_modified",
        "resource_time_last_read",
        "resource_value",
        "resource_value_default",
        "resource_value_type",
    ]

    methods: dict[str, callable] = {
        "CLOSE": None,
        "READ": None,
        "CREATE": None,
        "UPDATE": None,
        "SET": None,
        "RESET": None,
        "LOCK": None,
        "UNLOCK": None,
        "STAT": None,
        "CALL": None,
    }

    def __init__(self, application_database_instance):
        self.methods = {
            "CLOSE": self.resource_close,
            "READ": self.resource_read,
            "CREATE": self.resource_create,
            "UPDATE": self.resource_update,
            "SET": self.resource_set,
            "RESET": self.resource_reset,
            "LOCK": self.resource_lock,
            "UNLOCK": self.resource_unlock,
            "STAT": self.resource_stat,
            "CALL": self.resource_call,
        }

        self.database_instance = application_database_instance

    def method_call(self, method_key: str, *args):
        method_key = method_key.upper()

        if method_key in self.methods:
            self.methods[method_key](*args)
        else:
            raise ValueError(f"The method '{method_key}' is not a valid method.")

    def resource_close():
        """
        This method will notify the receiving connection to close its route, and
        end all traffic with the sender.
        """

        pass

    def resource_read():
        """
        Requests the value of a resource.
        """

        pass

    def resource_create(self, resource_name: str):
        """
        Creates a new resource in the collection associated with the connection
        route.
        """

        print(f":: Creating {resource_name}")

        self.database_instance.insert({"resource_name": resource_name})

    def resource_update():
        """
        Submits the value of a resource. Causes side-effects which may mutate
        additional resources or data.
        """

        pass

    def resource_set():
        """
        Submits the value of a resource, without causing any side-effects. SET
        is idempotent, whereas an UPDATE call might result in different data
        depending on the result.
        """

        pass

    def resource_reset():
        """
        Reset the value of a resource to its default value, as determined
        through the daemon.
        """

        pass

    def resource_lock():
        """
        Lock a resource, prevent its value from being modified.
        """

        pass

    def resource_unlock():
        """
        Unlocks a resource, allows its value to be modified.
        """

        pass

    def resource_stat():
        """
        Requests all metadata associated with a resource.
        """

        pass

    def resource_call():
        """
        Requests the execution of an RPC method, defined within the resource.
        """

        pass


class MolecularApplication:
    ipc_instance = None
    database_path: str = ""
    database_instance = None
    resource_manager = None

    def __init__(self, database_path: str):
        self.ipc_instance = molaccesspy.ManagedConsumer("molaccess-ipc-route-test")
        self.database_path = database_path
        self.database_instance = TinyDB(database_path)
        self.resource_manager = MolecularResourceManager(self.database_instance)

    def application_on_update(data_input: str):
        print(
            f":: Called callback function.\n:: Client received the following: '{data_input}'"
        )

        # To do:
        # - Parse string as JSON
        # - Parse for message methods
        # - Manipulate resources and collections

    def application_run(self):
        # ipc_instance.subscribe_update(self.application_on_update)
        self.resource_manager.resource_create("Test")
        self.resource_manager.method_call("CREATE", "Test2")


def main():
    molaccessd_application_instance = MolecularApplication("../../test-database.json")
    molaccessd_application_instance.application_run()


if __name__ == "__main__":
    main()
