import re
from commands import Command

current_deck = None

command_pattern = "!(\S)(\S*)\s*(.*)"

with open("test/anki_test.txt", "r") as f:
        lines = f.readlines()


current_command = None

def start_command(command):
    global current_command
    if current_command: current_command.do()
    current_command = command if not command.done else None

for line in lines:
    if len(line) > 0 and line.startswith("!"):
        action, args, body = re.match(command_pattern, line).groups()
        start_command(Command.create(action, args, body))
    elif current_command:
        current_command += line
if current_command: current_command.do()