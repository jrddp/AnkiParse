import re
from commands import Command

command_pattern = "!(\S)(\S*)\s*(.*)"

def analyze(file):
    current_command = None

    def start_command(command):
        nonlocal current_command
        if current_command: current_command.do()
        current_command = command if not command.done else None

    for line in file.readlines():
        if len(line) > 0 and line.startswith("!"):
            action, args, body = re.match(command_pattern, line).groups()
            start_command(Command.create(action, args, body))
        elif current_command:
            current_command += line
    if current_command: current_command.do()