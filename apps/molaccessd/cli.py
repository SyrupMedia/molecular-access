#!/usr/bin/env python3

"""
The entrypoint for the `molaccessd` process, meant to be run as an executable.
This file should not be imported as a module.
"""

import argparse
import datetime
import json
import os
import sys
import threading

from dataclasses import dataclass
from queue import Queue

import molaccesspy

from tinydb import TinyDB, Query


class MolecularDaemonConnectionThread(threading.Thread):
    def __init__(self, ipc_instance_route, messaging_queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)

        self.ipc_instance_route = ipc_instance_route
        self.messaging_queue = messaging_queue

    def run(self):
        """
        This is the target entrypoint for threads generated using the
        `ANNOUNCE` procedure. It maintains an IPC producer in order to send
        messages back to announced connections.
        """

        ipc_instance = molaccesspy.ManagedProducer(self.ipc_instance_route)

        print(f":: Created new producer thread on route `{self.ipc_instance_route}`.")

        while True:
            queue_message = self.messaging_queue.get()

            if queue_message is None:  # A None value will close the thread.
                break

            print(queue_message)


class MolecularDaemonConnection:
    ipc_instance_route: str = ""
    resource_collection: str = ""
    ipc_producer_thread: MolecularDaemonConnectionThread = None
    messaging_queue: Queue = None

    def __init__(self, ipc_instance_route, resource_collection):
        self.resource_collection = resource_collection
        self.ipc_instance_route = ipc_instance_route
        self.messaging_queue = Queue()

        self.ipc_producer_thread = MolecularDaemonConnectionThread(
            ipc_instance_route, self.messaging_queue
        )

    def connection_start(self):
        self.ipc_producer_thread.start()


class MolecularProcedureArguments:
    """
    This class carries the arguments passed to Molecular procedures, along with
    procedures to modify, validate, and generate arguments. This class exists in
    order to design around edge cases surrounding the way arguments are passed
    to procedures when matched, given procedures are strings in a dictionary
    matched to procedures, rather than procedures which should be called normally.
    """

    argument_dictionary: dict = {
        "resource_collection": "Molecular:Default",
        "resource_procedures_allowed": "ALL",
        "resource_procedures_provided": [],
        "resource_name": "",
        "connection_route": "",
        "resource_state_callable": False,
        "resource_state_locked": True,
        "resource_value": None,
        "resource_value_default": None,
        "resource_value_type": "",
    }

    def argument_dictionary_refresh(self) -> dict:
        """
        Set the `argument_dictionary` values to equal the values of their
        corresponding variables. Returns an updated dictionary.
        """

        argument_dictionary_new = {
            "resource_collection": self.resource_collection,
            "resource_procedures_allowed": self.resource_procedures_allowed,
            "resource_procedures_provided": self.resource_procedures_provided,
            "resource_name": self.resource_name,
            "connection_route": self.connection_route,
            "resource_state_callable": self.resource_state_callable,
            "resource_state_locked": self.resource_state_locked,
            "resource_value": self.resource_value,
            "resource_value_default": self.resource_value_default,
            "resource_value_type": self.resource_value_type,
        }

        self.argument_dictionary = argument_dictionary_new

        return argument_dictionary_new

    # This is insane, don't replicate this.
    # To do: Refactor how we set the variables of this class from a dictionary object.
    def argument_dictionary_set(self, argument_dictionary):
        """
        Sets the variables of this class to the values of corresponding keys.
        """

        for argument in self.argument_dictionary:
            if argument not in argument_dictionary:
                pass
            else:
                match argument:
                    case "resource_collection":
                        self.resource_collection = argument_dictionary[
                            "resource_collection"
                        ]
                    case "resource_procedures_allowed":
                        self.resource_procedures_provided = argument_dictionary[
                            "resource_procedures_allowed"
                        ]
                    case "resource_procedures_provided":
                        self.resource_procedures_provided = argument_dictionary[
                            "resource_procedures_allowed"
                        ]
                    case "resource_name":
                        self.resource_name = argument_dictionary["resource_name"]
                    case "connection_route":
                        self.connection_route = argument_dictionary["connection_route"]
                    case "resource_state_callable":
                        self.resource_state_callable = argument_dictionary[
                            "resource_state_callable"
                        ]
                    case "resource_state_locked":
                        self.resource_state_locked = argument_dictionary[
                            "resource_state_locked"
                        ]
                    case "resource_value":
                        self.resource_value = argument_dictionary["resource_value"]
                    case "resource_value_default":
                        self.resource_value_default = argument_dictionary[
                            "resource_value_default"
                        ]
                    case "resource_value_type":
                        self.resource_value_type = argument_dictionary[
                            "resource_value_type"
                        ]

    def __init__(
        self,
        resource_collection: str = "Molecular:Default",
        resource_procedures_allowed: str = "ALL",
        resource_procedures_provided: list = None,
        resource_name: str = "",
        connection_route: str = "",
        resource_state_callable: bool = False,
        resource_state_locked: bool = False,
        resource_value: any = None,
        resource_value_default: any = None,
        resource_value_type: str = "",
    ):
        self.resource_collection = resource_collection
        self.resource_procedures_allowed = resource_procedures_allowed
        self.resource_procedures_provided = resource_procedures_provided
        self.resource_name = resource_name
        self.connection_route = connection_route
        self.resource_state_callable = resource_state_callable
        self.resource_state_locked = resource_state_locked
        self.resource_value = resource_value
        self.resource_value_default = resource_value_default
        self.resource_value_type = resource_value_type


class MolecularResourceManager:
    """
    This class abstracts resource manipulation procedures, and serves as the
    core of `molaccessd`.
    """

    ipc_connections: dict[str:MolecularDaemonConnection]

    application_ipc_instance = None
    database_instance = None
    database_query_instance = None

    resource_keys: list[str] = [
        "resource_collection",
        "resource_name",
        "resource_procedures_allowed",
        "resource_procedures_provided",
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

    procedures: dict[str, callable] = {
        "ANNOUNCE": None,
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

    def __init__(
        self,
        application_ipc_instance,
        application_database_instance,
        application_database_query_instance,
    ):
        self.procedures = {
            "ANNOUNCE": self.resource_announce,
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

    def procedure_call(self, procedure_key: str, _argument_dictionary):
        """
        Calls a procedure's matching Python method by matching its name to a
        method stored inside of a dictionary.
        """

        procedure_key = procedure_key.upper()

        if procedure_key in self.procedures:
            self.procedures[procedure_key](_argument_dictionary)
        else:
            raise ValueError(
                f"The procedure '{procedure_key}' is not a valid procedure."
            )

    def procedure_call_json(self, data_input_string: str):
        """
        Calls a procedure method using a dictionary constructed from a JSON string.
        """

        data_input = json.loads(data_input_string)

        print(data_input)

        data_input_procedure = data_input["message"]["method"]
        data_input_arguments = data_input["message"]["arguments"]

        print(f"data_input_arguments: {data_input_arguments}")

        data_input_arguments_object = MolecularProcedureArguments()
        data_input_arguments_object.argument_dictionary_set(data_input_arguments)

        self.procedure_call(data_input_procedure, data_input_arguments_object)

    def resource_dictionary_create(
        self,
        resource_name,
        resource_value,
        resource_value_default,
        resource_value_type,
        resource_collection="Molecular:Default",
        resource_procedures_allowed="ALL",
        resource_procedures_provided=None,
        resource_state_callable=False,
        resource_state_locked=False,
    ) -> dict:
        """
        Creates a resource dictionary from arguments passed to this method.
        """

        datetime_now_string = str(datetime.datetime.now())

        new_resource_dictionary: dict = {
            "resource_collection": resource_collection,
            "resource_procedures_allowed": resource_procedures_allowed,
            "resource_procedures_provided": resource_procedures_provided,
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

    def resource_announce(
        self, molecular_procedure_arguments: MolecularProcedureArguments
    ):
        """
        This procedure will notify the receiving connection to start a route,
        and request traffic to and from the sender.
        """

        molecular_daemon_connection = MolecularDaemonConnection(
            ipc_instance_route=molecular_procedure_arguments.connection_route,
            resource_collection=molecular_procedure_arguments.resource_collection,
        )

        self.ipc_connections = {
            molecular_procedure_arguments.resource_collection: molecular_daemon_connection
        }

        molecular_daemon_connection.connection_start()

    def resource_close(self):
        """
        This procedure will notify the receiving connection to close its route, and
        end all traffic with the sender.
        """

    def resource_read(self, molecular_procedure_arguments: MolecularProcedureArguments):
        """
        Requests the value of a resource.
        """

        resource_query = self.database_instance.search(
            self.database_query_instance.resource_name
            == molecular_procedure_arguments.resource_name
        )

        if resource_query:
            # To do:
            # 1. Match resource's data to `ipc_connections` for relevant thread
            # 2. Submit data to the thread object's queue
            # 3. Read that data from the queue and send it back

            print(
                f"\n:: [{resource_query[0]['resource_name']}]\n:: Value: '{resource_query[0]['resource_value']}'\n"
            )

            resource_collection = resource_query[0]["resource_collection"]
            print(f":: Collection: {resource_collection}")

            print(f":: Connections:\n{self.ipc_connections}")

    def resource_create(
        self, molecular_procedure_arguments: MolecularProcedureArguments
    ):
        """
        Creates a new resource in the collection associated with the connection
        route.
        """

        if not molecular_procedure_arguments.resource_value_type in self.resource_types:
            raise ValueError(
                f"The type '{molecular_procedure_arguments.resource_value_type}' is not supported."
            )

        resource_query = self.database_instance.search(
            self.database_query_instance.resource_name
            == molecular_procedure_arguments.resource_name
        )

        if not resource_query:
            print(f":: Creating {molecular_procedure_arguments.resource_name}")

            new_resource_dictionary = self.resource_dictionary_create(
                resource_name=molecular_procedure_arguments.resource_name,
                resource_value=molecular_procedure_arguments.resource_value,
                resource_value_default=molecular_procedure_arguments.resource_value_default,
                resource_collection=molecular_procedure_arguments.resource_collection,
                resource_value_type=molecular_procedure_arguments.resource_value_type,
            )

            new_resource_dictionary_json_string = json.dumps(new_resource_dictionary)
            print(new_resource_dictionary_json_string)

            self.database_instance.insert(new_resource_dictionary)
        else:
            print(
                f":: A resource with the name {molecular_procedure_arguments.resource_name} already exists!"
            )

    def resource_update(self):
        """
        Submits the value of a resource. Causes side-effects which may mutate
        additional resources or data.
        """

    # To do: Reduce code duplication
    def resource_set(self, molecular_procedure_arguments: MolecularProcedureArguments):
        """
        Submits the value of a resource, without causing any side-effects. SET
        is idempotent, whereas an UPDATE call might result in different data
        depending on the result.
        """

        if not molecular_procedure_arguments.resource_value_type in self.resource_types:
            raise ValueError(
                f"The type '{molecular_procedure_arguments.resource_value_type}' is not supported."
            )

        resource_query = self.database_instance.search(
            self.database_query_instance.resource_name
            == molecular_procedure_arguments.resource_name
        )

        if not resource_query:
            print(
                f":: Error: Could not find {molecular_procedure_arguments.resource_name}"
            )
        else:
            new_resource_dictionary = self.resource_dictionary_create(
                resource_name=molecular_procedure_arguments.resource_name,
                resource_value=molecular_procedure_arguments.resource_value,
                resource_value_default=molecular_procedure_arguments.resource_value_default,
                resource_value_type=molecular_procedure_arguments.resource_value_type,
            )

            # To do: Debug mode to print these strings to stdout
            new_resource_dictionary_json_string = json.dumps(
                molecular_procedure_arguments.argument_dictionary
            )
            print(new_resource_dictionary_json_string)

            self.database_instance.update(new_resource_dictionary)

    def resource_reset(self):
        """
        Reset the value of a resource to its default value, as determined
        through the daemon.
        """

    def resource_lock(self):
        """
        Lock a resource, prevent its value from being modified.
        """

    def resource_unlock(self):
        """
        Unlocks a resource, allows its value to be modified.
        """

    def resource_stat(self):
        """
        Requests all metadata associated with a resource.
        """

    def resource_call(self):
        """
        Requests the execution of an RPC procedure, defined within the resource.
        """


class MolecularDaemon:
    """
    The `molaccessd` class, abstracting all functionality of the application.
    """

    ipc_instance = None
    ipc_instance_route: str = "molaccessd"
    database_path: str = ""
    database_instance = None
    database_query_instance = None
    resource_manager = None
    arguments = None

    def __init__(self, database_path: str, ipc_instance_route: str = None):
        if ipc_instance_route:
            self.ipc_instance_route = ipc_instance_route

        self.ipc_instance = molaccesspy.ManagedConsumer(self.ipc_instance_route)
        self.database_path = database_path
        self.database_instance = TinyDB(database_path)
        self.database_query_instance = Query()
        self.resource_manager = MolecularResourceManager(
            self.ipc_instance, self.database_instance, self.database_query_instance
        )

    def arguments_create(self):
        argument_parser = argparse.ArgumentParser(
            prog="molmessg",
            description="The Molecular Access daemon, a background process which receives and outputs Molecular messages.",
        )
        argument_parser.add_argument(
            "-r",
            "--route",
            default="molaccessd",
            help="The IPC route which should be used for communications. This value must be the same across any process using Molecular! Changing this value is NOT recommended.",
        )

        self.arguments = argument_parser.parse_args()

        self.ipc_instance_route = self.arguments.route

    def application_on_update(self, data_input: str):
        """
        This is a callback function called from the low-level Molecular C++ API
        whenever an IPC message is received.
        """

        print(f":: Received message: `{data_input}`")

        self.resource_manager.procedure_call_json(data_input)

        print(
            f":: Called callback function.\n:: Client received the following: '{data_input}'"
        )

    def application_run(self):
        """
        Runs the `molaccessd` core update loop.
        """

        while True:
            try:
                self.ipc_instance.subscribe_update(self.application_on_update)
            except KeyboardInterrupt:
                break


def main():
    print(f":: Running `molaccessd` with PID `{os.getpid()}`.")

    molaccessd_application_instance = MolecularDaemon("../../test-database.json")
    molaccessd_application_instance.arguments_create()
    molaccessd_application_instance.application_run()


if __name__ == "__main__":
    main()
