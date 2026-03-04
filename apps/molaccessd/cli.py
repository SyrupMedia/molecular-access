#!/usr/bin/env python3

"""
The entrypoint for the `molaccessd` process, meant to be run as an executable.
This file should not be imported as a module.
"""

import molaccesspy


class MolecularResourceManager:
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
        "CLOSE": resource_close(),
        "READ": resource_read(),
        "CREATE": resource_create(),
        "UPDATE": resource_update(),
        "SET": resource_set(),
        "RESET": resource_reset(),
        "LOCK": resource_lock(),
        "UNLOCK": resource_unlock(),
        "STAT": resource_stat(),
        "CALL": resource_call(),
    }

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

    def resource_create():
        """
        Creates a new resource in the collection associated with the connection
        route.
        """

        pass

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

    def __init__(self):
        self.ipc_instance = molaccesspy.ManagedConsumer("molaccess-ipc-route-test")

    def application_on_update(data_input: str):
        print(
            f":: Called callback function.\n:: Client received the following: '{data_input}'"
        )

        # To do:
        # - Parse string as JSON
        # - Parse for message methods
        # - Manipulate resources and collections

    def application_run(self):
        ipc_instance.subscribe_update(self.application_on_update)


def main():
    pass


if __name__ == "__main__":
    main()
