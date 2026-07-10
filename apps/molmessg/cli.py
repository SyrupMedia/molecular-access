import argparse
import sys
import json
import os
import threading

import molaccesspy


def message_create(method: str, argument_dictionary: dict) -> dict:
    print(argument_dictionary)
    new_message = {"message": {"method": str(method), "arguments": argument_dictionary}}

    return new_message


class ConsumerThread(threading.Thread):
    def __init__(self, ipc_instance_route, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)

        self.ipc_instance_route = ipc_instance_route

    def on_update(self, data: str):
        print("Updated thread.")
        print(data)

    def run(self):
        print(f":: Creating new consumer thread on route `{self.ipc_instance_route}`.")

        ipc_instance = molaccesspy.ManagedConsumer(self.ipc_instance_route)
        ipc_instance.subscribe_update(self.on_update)


class CommandManager:
    commands: list = ["HELP", "SEND", "JSEND", "EXIT"]
    is_announced: bool = False
    announced_route = ""

    application_ipc_instance = None

    def __init__(self, messaging_ipc_instance):
        self.application_ipc_instance = messaging_ipc_instance

    def command_help(self):
        help_message = """
        Syntax: [COMMAND] [ARGUMENTS]
        Commands:
            'HELP' : Display this message.
            'SEND' : Send a message to `molaccessd`. Space-seperated arguments will be concatenated into a JSON string.
            'JSEND' : Send a raw JSON string to `molaccessd`. Expects JSON-formatted string as argument.
            'EXIT' : Safely exits this program."""

        print(help_message)

    def command_send(self, method_argument_string, argument_dictionary):
        message = message_create(method_argument_string, argument_dictionary)
        message_json = json.dumps(message)

        create_consumer = False
        is_announcing: bool = False
        procedure = message["message"]["method"]

        # Check if the procedure call to be sent out requires a ManagedConsumer
        match procedure:
            case "READ":
                create_consumer = True
            case "STAT":
                create_consumer = True
            case "ANNOUNCE":
                self.announced_route = message["message"]["arguments"][
                    "connection_route"
                ]
                is_announcing = True
            case _:
                pass

        # If it does, create one in a new thread with the route passed in the message
        # The route specified should never equal `molaccessd`, and `molaccessd`'s
        # newly created ManagedProducer should send data back to the route specified
        # by the message sent from `molmessg`.
        if is_announcing and self.is_announced:
            print(
                ":: Error: `ANNOUNCE` procedure may not be called, this instance has already been announced."
            )
        elif is_announcing:
            print(f":: Announcing this instance as {self.announced_route}")
            self.is_announced = True

        if create_consumer:
            if not self.is_announced:
                print(
                    ":: Error: The `READ` or `STAT` procedures may not be called without having announced."
                )

                return

            print(
                f":: Procedure `{procedure}` requires a consumer, creating one in a new thread."
            )

            consumer_thread = ConsumerThread(self.announced_route)
            consumer_thread.start()

        self.application_ipc_instance.send_data(str(message_json))

        if create_consumer:
            consumer_thread.join()

    def command_send_json(self, json_string):
        self.application_ipc_instance.send_data(str(json_string))

    def command_exit(self):
        sys.exit(0)


class MolecularMesssagingBase:
    application_ipc_instance = None
    command_manager = None
    command_dictionary: dict[str, callable] = None
    should_loop = True
    arguments = None
    ipc_instance_route: str = "molaccessd"

    def __init__(self):
        self.application_ipc_instance = molaccesspy.ManagedProducer(
            self.ipc_instance_route
        )
        self.command_manager = CommandManager(self.application_ipc_instance)

        self.command_dictionary: dict[str, callable] = {
            "HELP": self.command_manager.command_help,
            "SEND": self.command_manager.command_send,
            "JSEND": self.command_manager.command_send_json,
            "EXIT": self.command_manager.command_exit,
        }

    def call_command(self, data_input_raw: str):
        if not data_input_raw or len(data_input_raw) < 1:
            return

        data_input = data_input_raw.split()
        command = data_input[0]
        command_arguments = data_input[2:]
        command_arguments_dictionary = {}

        for argument in command_arguments:
            argument = argument.split("=")
            command_arguments_dictionary[argument[0]] = argument[1]

        if command not in self.command_manager.commands:
            self.command_manager.command_help()
        else:
            if command == "HELP":
                self.command_manager.command_help()
            elif command == "EXIT":
                self.command_manager.command_exit()
            elif command == "SEND":
                self.command_manager.command_send(
                    data_input[1], command_arguments_dictionary
                )
            else:
                # Match first element of list to command dictionary, and provide the rest of the list as arguments.
                self.command_dictionary[command](command_arguments)

    def arguments_create(self):
        argument_parser = argparse.ArgumentParser(
            prog="molmessg",
            description="An interactive interpreter shell (REPL) for Molecular, allowing you to send IPC messages to processes connected to molaccessd.",
        )
        argument_parser.add_argument(
            "-c",
            "--command",
            help="Pass a string to be interpreted; similar to `bash -c`, `python -c`, etc.",
        )
        argument_parser.add_argument(
            "-r",
            "--route",
            default="molaccessd",
            help="The IPC route which should be used for communications. This value must be the same across any process using Molecular! Changing this value is NOT recommended.",
        )
        argument_parser.add_argument(
            "script",
            help="A `molmsg` script to parse commands from.",
        )

        self.arguments = argument_parser.parse_args()

        self.ipc_instance_route = self.arguments.route

    def message(self):
        if self.should_loop:
            while self.should_loop:
                data_input_raw: str = str(input("molmessg shell: "))

                self.call_command(data_input_raw)
        elif self.arguments.command:
            self.call_command(str(self.arguments.command))
        elif self.arguments.script:
            line_count: int = 0
            
            with open(
                file=f"{self.arguments.script}", mode="r", encoding="utf-8"
            ) as script_file:
                script_string: str = script_file.readlines()

                for line in script_string:
                    line_count += 1

                    print(f"Parsing line {line_count}:   \n{line}")

                    # ignore comments
                    if line.startswith("#"):
                        pass
                    elif not line:
                        pass
                    else:
                        # To do: Support semicolons.
                        # if ';' in line
                        # # Check if semicolon is in between qoutes or not.
                        # # If it isn't then treat it as a delimiter between commands.
                        # pass

                        command = str(line).split()

                        if command:
                            command = command[0]

                            # Check if the first word of the line is a valid command
                            if command in CommandManager.commands:
                                self.call_command(str(line))
                            else:
                                # To do: Unified way to safely throw errors.
                                raise Exception(f"Command `{command}` is not a valid command.")


def main():
    print(f":: Running `molmessg` with PID `{os.getpid()}`.")

    molecular_messaging_base_instance = MolecularMesssagingBase()
    molecular_messaging_base_instance.arguments_create()

    if molecular_messaging_base_instance.arguments.command:
        molecular_messaging_base_instance.should_loop = False
    elif molecular_messaging_base_instance.arguments.script:
        molecular_messaging_base_instance.should_loop = False

    try:
        molecular_messaging_base_instance.message()
    except KeyboardInterrupt:
        molecular_messaging_base_instance.should_loop = False


if __name__ == "__main__":
    main()
