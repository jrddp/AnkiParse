import re
from pathlib import Path

from cards import Card
from commands import Command

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

        for i, line in enumerate(file.readlines()):
            if len(line) > 0 and line.startswith("!"):
                action, args, body = re.match(command_pattern, line).groups()
                try:
                    start_command(Command.create(action, args, body, start_index=i))
                except ValueError:
                    pass
                else:
                    continue
            if current_command is not None:
                current_command += line

        if current_command: current_command.do()
        from cards import current_card
        if current_card: current_card.close(i)


def replace_with_note_formatting(file_lines: list[str], cards: list[Card] = Card.closed_cards):
    lines = file_lines.copy()
    offset = 0
    for card in cards:
        start_i, end_i = card.line_range

        # lines[start_i] += " [ANKI_START]"
        # lines[end_i] += " [ANKI_END]"

        start_i += offset
        end_i += offset

        del lines[start_i:end_i + 1]
        lines.insert(start_i, card.get_note_formatted_string())
        offset -= end_i - start_i
    return lines
