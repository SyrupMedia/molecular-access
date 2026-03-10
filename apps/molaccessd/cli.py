#!/usr/bin/env python3

"""
The entrypoint for the `molaccessd` process, meant to be run as an executable.
This file should not be imported as a module.
"""

import datetime
import json

import molaccesspy

from tinydb import TinyDB, Query


class MolecularResourceManager:
    application_ipc_instance = None
    database_instance = None
    database_query_instance = None

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

    resource_types: dict[str, type] = {
        "bool": bool,
        "string": str,
        "int": int,
        "float": float,
    }

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

    def __init__(self, application_ipc_instance, application_database_instance, application_database_query_instance):
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

        self.application_ipc_instance = application_ipc_instance
        self.database_instance = application_database_instance
        self.database_query_instance = application_database_query_instance

    def method_call(self, method_key: str, *args):
        method_key = method_key.upper()

        if method_key in self.methods:
            self.methods[method_key](*args)
        else:
            raise ValueError(f"The method '{method_key}' is not a valid method.")

    def resource_dictionary_create(
        self,
        resource_name,
        resource_value,
        resource_value_default,
        resource_value_type,
        resource_collection="Molecular:Default",
        resource_methods_allowed="ALL",
        resource_methods_provided=None,
        resource_state_callable=False,
        resource_state_locked=False,
    ) -> dict:

        datetime_now_string = str(datetime.datetime.now())

        new_resource_dictionary: dict = {
            "resource_collection": resource_collection,
            "resource_methods_allowed": resource_methods_allowed,
            "resource_methods_provided": resource_methods_provided,
            "resource_name": resource_name,
            "resource_state_callable": resource_state_callable,
            "resource_state_locked": resource_state_locked,
            "resource_time_creation": datetime_now_string,
            "resource_time_last_modified": datetime_now_string,
            "resource_time_last_read": datetime_now_string,
            "resource_value": resource_value,
            "resource_value_default": resource_value_default,
            "resource_value_type": resource_value_type,
        }

        return new_resource_dictionary

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

    def resource_create(
        self,
        new_resource_name,
        new_resource_value,
        new_resource_value_default,
        new_resource_value_type,
    ):
        """
        Creates a new resource in the collection associated with the connection
        route.
        """

        if not new_resource_value_type in self.resource_types:
            raise ValueError(f"The type '{resource_value_type}' is not supported.")

        resource_query = self.database_instance.search(self.database_query_instance.resource_name == new_resource_name)

        if not resource_query:
            print(f":: Creating {new_resource_name}")

            new_resource_dictionary = self.resource_dictionary_create(
                resource_name=new_resource_name,
                resource_value=new_resource_value,
                resource_value_default=new_resource_value_default,
                resource_value_type=new_resource_value_type,
            )

            new_resource_dictionary_json_string = json.dumps(new_resource_dictionary)

            self.database_instance.insert(new_resource_dictionary)
        else:
            print(f":: A resource with the name {new_resource_name} already exists!")

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
    ipc_instance_route: str = "molaccessd"
    database_path: str = ""
    database_instance = None
    database_query_instance = None
    resource_manager = None

    def __init__(self, database_path: str, ipc_instance_route: str = None):
        if ipc_instance_route:
            self.ipc_instance_route = ipc_instance_route

        self.ipc_instance = molaccesspy.ManagedConsumer(self.ipc_instance_route)
        self.database_path = database_path
        self.database_instance = TinyDB(database_path)
        self.database_query_instance = Query()
        self.resource_manager = MolecularResourceManager(self.ipc_instance, self.database_instance, self.database_query_instance)

    def application_on_update(self, data_input: str):
        print(
            f":: Called callback function.\n:: Client received the following: '{data_input}'"
        )

        try:
            data_dictionary = json.loads(str(data_input))
        except json.decoder.JSONDecodeError:
            print(":: Error: Failed to serialize JSON string into a dict object!")

        # To do:
        # - Parse string as JSON
        # - Parse for message methods
        # - Manipulate resources and collections

    def application_run(self):
        self.ipc_instance.subscribe_update(self.application_on_update)
        
        #self.resource_manager.resource_create(
        #    new_resource_name="Test",
        #    new_resource_value="This is a value!",
        #    new_resource_value_default="This is a default value!",
        #    new_resource_value_type="string",
        #)

        #self.resource_manager.method_call("CREATE",
        #    "Test2",
        #    "This is another value!",
        #    "This is another default value!",
        #    "string"
        #)

        # To do:
        # - Listen for new IPC producers which attempt to establish a connection, 
        # then create a producer in a new thread to send data back to them
        # - Listen for messages, and call methods by matching from a JSON dictionary object


def main():
    molaccessd_application_instance = MolecularApplication("../../test-database.json")
    molaccessd_application_instance.application_run()


if __name__ == "__main__":
    main()
