#!/bin/env python3

def latex_to_mathjax(string: str):
    import re

    string = re.sub(r"\$\$(.*?)\$\$", r"\[\1\]", str(string))
    string = re.sub(r"\$(.*?)\$", r"\(\1\)", str(string))
    return string

class Card:

    def __init__(self, deck: str, model: str, fields: dict, tags: list):
        self.deck = deck
        self.model = model
        self.fields = fields
        self.tags = tags

    @staticmethod
    def create(deck, text1: str, text2: str, tags, convert_latex_to_mathjax=True, double=False):
        import re

        if convert_latex_to_mathjax:
            text1 = latex_to_mathjax(text1)
            text2 = latex_to_mathjax(text2)

        text1 = text1.replace("\n", "<br \\>")
        text2 = text2.replace("\n", "<br \\>")

        cloze = bool(re.search(r'\{\{c\d+::(?:.+?)\}\}', text1))
        if cloze:
            return ClozeCard(deck=deck, text=text1, back_extra=text2, tags=tags)
        else:
            return BasicCard(deck=deck, front=text1, back=text2, tags=tags, and_reversed=double)

    def send_to_anki(self):
        import requests

        r = requests.post('http://127.0.0.1:8765', json={
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deck,
                    "modelName": self.model,
                    "fields": self.fields,
                    "tags": self.tags if self.tags else []
                }
            }
        })

        err = r.json()['error']
        if err:
            raise RuntimeError(f"{err} ({self})")
        print(f"Uploaded card to {self.deck}")

    def __str__(self):
        return f"{self.model} from {self.deck}\n{self.fields}\nTags: {self.tags}"


class BasicCard(Card):

    def __init__(self, deck: str, front: str, back: str, tags: list, and_reversed=False):
        super().__init__(deck, model="Basic" + (" (and reversed card)" if and_reversed else ""),
                         fields={"Front": front, "Back": back}, tags=tags)


class ClozeCard(Card):

    def __init__(self, deck: str, text: str, back_extra: str, tags: list):
        super().__init__(deck=deck, model="Cloze", fields={"Text": text, "Back Extra": back_extra}, tags=tags)


# commands
# d: set the current deck
# q: write the front/question text
# a: write the back/answer text
# r: replace replace_str with followed

replace_str = "?"
repl_strip = ","


def analyze(file_path):
    cards = []
    with open(file_path, "r") as f:
        deck = "Default"
        front = ""
        back = ""
        tags = []

        mode = ""
        arg_double = False

        def complete_card():
            nonlocal deck, front, back, tags, arg_double
            cards.append(Card.create(deck, front, back, tags, double=arg_double))
            front = ""
            back = ""
            tags = []
            arg_double = False

        for line in f:
            line = line.rstrip()
            if line.startswith("!"):
                command = line[1]
                s_index = line.find(" ")
                args = line[2:line.find(" ")] if len(line) > 2 and s_index > 2 else ""
                if s_index == -1 and len(line) > 2:
                    args = line[2:]
                string = line[s_index:].lstrip() if s_index > -1 else ""

                if command == "!":
                    if "a" in args:
                        back = list(cards[-1].fields.values())[1]
                    if "t" in args:
                        tags = cards[-1].tags
                elif command == "d":
                    # deck = line.
                    if "d" in args or "e" in args:
                        deck = string
                    else:
                        deck = "::".join(string.title().split())
                elif command == "q":
                    if front:
                        complete_card()
                    front = string

                    if "q" in args:
                        arg_double = True

                    mode = "q"
                elif command == "r":
                    sequential = "s" in args
                    if string.count(replace_str) == 1:
                        front = front.replace(replace_str, "{{c1::%s}}" % string.strip(), 1)
                    else:
                        for i, repl in enumerate(string.split(repl_strip), 1):
                            front = front.replace(replace_str, "{{c%d::%s}}" % ((i if sequential else 1), repl.strip()), 1)
                elif command == "a":
                    back = string
                    mode = "a"
                elif command == "t":
                    tags = string.split()
            else:
                if mode == "q" or mode == "a":
                    if line:
                        if mode == "q":
                            front += ("\n" if front else "") + str(line)
                        else:
                            back += ("\n" if back else "") + str(line)

        complete_card()
    print(*cards, sep="\n-----\n")
    for card in cards:
        card.send_to_anki()


import sys
analyze(sys.argv[1])
