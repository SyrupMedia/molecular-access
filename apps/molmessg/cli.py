import argparse
import sys
import json
import os

import molaccesspy


def message_create(method: str, argument_dictionary: dict) -> dict:
    print(argument_dictionary)
    new_message = {"message": {"method": str(method), "arguments": argument_dictionary}}

    return new_message


class CommandManager:
    commands: list = ["HELP", "SEND", "JSEND", "EXIT"]

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

        self.application_ipc_instance.send_data(str(message_json))

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

    def __init__(self):
        self.application_ipc_instance = molaccesspy.ManagedProducer("molaccessd")
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
            argument = argument.split('=')
            command_arguments_dictionary[argument[0]] = argument[1]
        
        if command not in self.command_manager.commands:
            self.command_manager.command_help()
        else:
            if command == "HELP":
                self.command_manager.command_help()
            elif command == "EXIT":
                self.command_manager.command_exit()
            elif command == "SEND":
                self.command_manager.command_send(data_input[1], command_arguments_dictionary)
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
        self.arguments = argument_parser.parse_args()

    def message(self):
        if self.should_loop:
            while self.should_loop:
                data_input_raw: str = str(input("molmessg shell: "))

                self.call_command(data_input_raw)
        else:
            self.call_command(str(self.arguments.command))


def main():
    print(f":: Running `molmessg` with PID `{os.getpid()}`.")

    molecular_messaging_base_instance = MolecularMesssagingBase()
    molecular_messaging_base_instance.arguments_create()

    if molecular_messaging_base_instance.arguments.command:
        molecular_messaging_base_instance.should_loop = False

    try:
        molecular_messaging_base_instance.message()
    except KeyboardInterrupt:
        molecular_messaging_base_instance.should_loop = False


if __name__ == "__main__":
    main()
