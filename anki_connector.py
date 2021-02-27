# Gateway for using the AnkiConnect addon and interacting with the user's Anki profile

import requests

anki_connect_port = 'http://127.0.0.1:8765'


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


def create_anki_deck(deck: str):
    deck_add_json = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck
        }
    }

    r = requests.post(anki_connect_port, json=deck_add_json)
    response = r.json()
    if response['error']: raise RuntimeError(f"AnkiConnect: {response['error']}")
    else:
        print("Created Anki deck: " + deck)
