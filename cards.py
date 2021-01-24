import formatter


class Card:

    def __init__(self, front, back="", tags=None, model="Basic", add_reversed=False):
        if tags is None:
            tags = []

        self.deck = current_deck
        self.front = front
        self.back = back
        self.tags = tags
        self.model = model
        self.add_reversed = add_reversed

    def close(self):
        try:
            self.front = formatter.format_everything(self.front)
            self.back = formatter.format_everything(self.back)
            send_card_to_anki(self)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e.args}")
            pass
        else:
            print("Success!")
            pass


def send_card_to_anki(card):
    import requests

    if card.model == "Cloze":
        fields = {"Text": card.front, "Back Extra": card.back}
    else:  # Basic Cards
        fields = {"Front": card.front, "Back": card.back}

    r = requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": card.deck,
                "modelName": card.model,
                "fields": fields,
                "tags": card.tags
            }
        }
    })

    err = r.json()['error']
    if err:
        raise RuntimeError(f"{err}")
    print(f"Uploaded card to {card.deck}")


current_deck = None
current_card: Card = None
