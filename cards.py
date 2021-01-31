import formatter

# TODO Create reformatted text to replace in analyzed file with nice note format

anki_connect_port = 'http://127.0.0.1:8765'


class Card:

    def __init__(self, front, back="", tags=None, model="Basic", add_reversed=False):
        if tags is None:
            tags = []

        if (add_reversed): model = "Basic (and reversed card)"

        self.deck = current_deck
        self.front = front
        self.back = back
        self.tags = tags
        self.model = model
        self.add_reversed = add_reversed
        self.image_paths = set()

    def get_json(self):
        if self.model == "Cloze":
            fields = {"Text": self.front, "Back Extra": self.back}
        else:  # Basic Cards or Basic and Reversed Cards
            fields = {"Front": self.front, "Back": self.back}

        return {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deck,
                    "modelName": self.model,
                    "fields": fields,
                    "tags": self.tags
                }
            }
        }

    def close(self):
        try:
            self.image_paths = formatter.get_image_paths(self.front)
            self.image_paths.update(formatter.get_image_paths(self.back))

            self.front = formatter.format_everything(self.front)
            self.back = formatter.format_everything(self.back)
            send_card_to_anki(self)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e.args}")
            pass
        else:
            pass


def get_image_store_json(image_path):
    import formatter, analyzer
    is_url = formatter.is_url(image_path)
    if not is_url:
        image_path = analyzer.current_file_path.absolute().parent / image_path
    return {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": formatter.get_image_name(image_path),
            "url" if is_url else "path": str(image_path)
        }
    }


def send_card_to_anki(card):
    import requests

    if card.image_paths:
        actions = [get_image_store_json(p) for p in card.image_paths]
        actions.append(card.get_json())

        r = requests.post(anki_connect_port, json={
            "action": "multi",
            "params": {
                "actions": actions
            }
        })
    else:
        r = requests.post(anki_connect_port, json=card.get_json())

    # response can either be list or dict
    response = r.json()
    errors = [response['error']] if isinstance(r.json(), dict) else [r['error'] for r in response]
    if errors:
        for err in errors:
            if err is not None: raise RuntimeError(f"AnkiConnect: {err}")
    print(f"Uploaded card to {card.deck}")


current_deck = None
current_card: Card = None
