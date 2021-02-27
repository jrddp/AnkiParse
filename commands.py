import cards

# TODO add support for deck prompting when deck is missing
# TODO allow default decks based on directories

last_cmd_cache = {}

replacable_str = "___"
replacement_delim = "///"


class Command:
    action = ""
    multiline = False
    repeatable = False

    @classmethod
    def create(cls, action, args, body, start_index):
        for subcls in cls.__subclasses__():
            if action == subcls.action:
                return subcls(args, body, start_index)
        raise ValueError(f"{action} is an unrecognized action!")

    def __init__(self, args, body, start_index):
        self.args = args
        if body and self.multiline: body += "\n"
        self.body = body
        self.start_index = start_index
        self.done = False

    def __iadd__(self, other):
        self.body += other
        return self

    def do(self):
        if self.repeatable:
            last_cmd_cache[self.action] = self
        self.done = True


class CommandDeck(Command):
    action = "d"
    multiline = False

    def do(self):
        if "t" in self.args:
            cards.current_tags = self.body.split()
        else:
            if "c" in self.args:
                import anki_connector
                anki_connector.create_anki_deck(self.body)
            cards.current_deck = self.body
        super().do()


class CommandQuestion(Command):
    action = "q"
    multiline = True

    def do(self):
        if cards.current_card is not None: cards.current_card.close(self.start_index - 1)

        if ("t" in self.args or "f" in self.args):
            front = "**True or False?**\n" + self.body
            answer = "**" + str("t" in self.args) + "**\n" # True for t arg and f if f arg
            cards.current_card = cards.Card(front=front, back=str(answer), add_reversed="q" in self.args, start_index=self.start_index)
        else:
            cards.current_card = cards.Card(front=self.body, add_reversed=("q" in self.args), start_index=self.start_index)

        super().do()


class CommandAnswer(Command):
    action = "a"
    multiline = True
    repeatable = True

    def do(self):
        cards.current_card.back = cards.current_card.back + self.body
        super().do()


class CommandReplace(Command):
    action = "r"
    multiline = False

    def do(self):
        sequential = "s" in self.args
        text = cards.current_card.front
        count = text.count(replacable_str)
        if count == 1:
            text = text.replace(replacable_str, "{{c1::%s}}" % self.body.strip(), 1)
        else:
            for i, repl in enumerate(self.body.split(replacement_delim), 1):
                text = text.replace(replacable_str, "{{c%d::%s}}" % ((i if sequential else 1), repl.strip()), 1)
        cards.current_card.front = text
        cards.current_card.model = "Cloze"
        super().do()


class CommandTag(Command):
    action = "t"
    multiline = False
    repeatable = True

    def do(self):
        cards.current_card.tags = self.body.split()
        super().do()


class CommandFinalize(Command):
    action = "f"
    multiline = False

    def do(self):
        if cards.current_card is not None: cards.current_card.close(self.start_index)
        super().do()


class CommandRepeat(Command):
    action = "!"
    multiline = False

    def do(self):
        for action in self.args:
            if action in last_cmd_cache.keys():
                last_cmd_cache[action].do()
            else:
                raise ReferenceError(
                    f"Failed to repeat {action} command: It is either non-repeatable or not yet performed.")
        super().do()
