import sys
import json

import molaccesspy

def message_create(method: str, arguments: str) -> dict:
    new_message = {
        "message": {
            "method": str(method),
            "arguments": str(arguments)
        }
    }

    return new_message

class CommandManager:
    commands: list = [
        "HELP",
        "SEND",
        "JSEND",
        "EXIT"
    ]

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

    def command_send(self, arguments_list: list[str]):
        method_argument_string = arguments_list[0]
        arguments_string = arguments_list[1:]

        message = message_create(method_argument_string, arguments_string)
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


    def __init__(self):
        self.application_ipc_instance = molaccesspy.ManagedProducer("molaccessd")
        self.command_manager = CommandManager(self.application_ipc_instance)
        
        self.command_dictionary: dict[str, callable] = {
                "HELP": self.command_manager.command_help,
                "SEND": self.command_manager.command_send,
                "JSEND": self.command_manager.command_send_json,
                "EXIT": self.command_manager.command_exit
        }

    def call_command(self, data_input_raw: str):
        data_input = data_input_raw.split()
        command = data_input[0]
        command_arguments = data_input[1:]

        if command not in self.command_manager.commands:
            self.command_manager.command_help()
        else:
            if command == "HELP":
                self.command_manager.command_help()
            elif command == "EXIT":
                self.command_manager.command_exit()
            else:
                # Match first element of list to command dictionary, and provide the rest of the list as arguments.
                self.command_dictionary[command](command_arguments)

def main():
    molecular_messaging_base_instance = MolecularMesssagingBase()

    while True:
        data_input_raw: str = str(input("molmessg shell: "))
        
        molecular_messaging_base_instance.call_command(data_input_raw)

if __name__ == "__main__":
    main()
