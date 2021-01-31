import re
from commands import Command
from pathlib import Path

command_pattern = "!(\S)(\S*)\s*(.*)"
current_file_path: Path = None


def analyze(path: Path):
    global current_file_path
    current_file_path = path

    with open(path) as file:
        current_command = None

        def start_command(command):
            nonlocal current_command
            if current_command is not None: current_command.do()
            if command.multiline:
                current_command = command
            else:
                command.do()
                current_command = None

        for line in file.readlines():
            if len(line) > 0 and line.startswith("!"):
                action, args, body = re.match(command_pattern, line).groups()
                try:
                    start_command(Command.create(action, args, body))
                except ValueError:
                    pass
                else:
                    continue
            if current_command is not None:
                current_command += line

        if current_command: current_command.do()
        from cards import current_card
        if current_card: current_card.close()
