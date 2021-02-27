import formatter

anki_connect_port = 'http://127.0.0.1:8765'


class Card:
    closed_cards = []

    def __init__(self, front, start_index, back="", tags=None, model="Basic", add_reversed=False):
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
        self.line_range = [start_index, -1]

    def get_json(self):
        formatted_front = formatter.format_everything(self.front)
        formatted_back = formatter.format_everything(self.back)

        if self.model == "Cloze":
            fields = {"Text": formatted_front, "Back Extra": formatted_back}
        else:  # Basic Cards or Basic and Reversed Cards
            fields = {"Front": formatted_front, "Back": formatted_back}

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

    # This should be called before reformatting to HTML
    def get_note_formatted_string(self):
        from datetime import date
        if self.model == "Cloze":
            import re
            # Replace any Cloze deletions with bold text
            note_str = "> " + re.sub(r"{{c[0-9]+::(.+?)}}", r"<b>\1</b>", self.front.strip())
            if self.back: note_str += "\n\n" + self.back.strip()
        else:
            note_str = f"> <b>{self.front.strip()}</b>\n\n{self.back.strip()}"

        note_str = note_str.replace("\n", " \n> ")

        date_str = date.today().strftime('%m/%d/%Y')
        add_tag = f"Added to Anki deck '{self.deck}' on {date_str}"
        add_tag = f"> <i><sub>{add_tag}</sub></i>"

        note_str += " \\\n" + add_tag

        return "\n" + note_str + "\n"

    def close(self, end_index):
        global current_card
        if self == current_card: current_card = None

        try:
            self.line_range[1] = end_index

            self.image_paths = formatter.get_image_paths(self.front)
            self.image_paths.update(formatter.get_image_paths(self.back))

            send_card_to_anki(self)
            Card.closed_cards.append(self)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e.args}")


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
