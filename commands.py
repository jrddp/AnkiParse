actions = "dqartf"
multiline_actions = "qa"


class Command:
    action = ""
    multiline = True

    @classmethod
    def create(cls, action, args, body):
        for subcls in cls.__subclasses__():
            if action == subcls.action:
                return subcls(args, body)
        raise ValueError(f"{action} is an unrecognized action!")

    def __init__(self, args, body):
        self.args = args
        self.body = body
        self.done = False

        if self.action not in multiline_actions:
            self.do()

    def __iadd__(self, other):
        self.body += other

    def do(self):
        print("Performed " + self.action)
        self.done = True


class CommandDeck(Command):
    action = "d"
    multiline = False

    def do(self):
        super().do()


class CommandQuestion(Command):
    action = "q"
    multiline = True

    def do(self):
        super().do()


class CommandAnswer(Command):
    action = "a"
    multiline = True

    def do(self):
        super().do()


class CommandReplace(Command):
    action = "r"
    multiline = False

    def do(self):
        super().do()


class CommandTag(Command):
    action = "t"
    multiline = False

    def do(self):
        super().do()


class CommandFinalize(Command):
    action = "f"
    multiline = False

    def do(self):
        super().do()