class Card:

    def __init__(self, front, back="", tags=None, cloze=False, add_reversed=False):
        if tags is None:
            tags = []

        self.deck = current_deck
        self.front = front
        self.back = back
        self.tags = tags
        self.is_cloze = cloze
        self.add_reversed = add_reversed

    def close(self):
        pass

current_deck = None
current_card: Card = None

class Card2:

    def __init__(self, deck: str, model: str, fields: dict, tags: list):
        self.deck = deck
        self.model = model
        self.fields = fields
        self.tags = tags

    @staticmethod
    def create(deck, text1: str, text2: str, tags, convert_latex_to_mathjax=True, double=False):

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