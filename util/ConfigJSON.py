import json


def token():
    try:

        with open("config.json", "r+") as config:
            try:
                data = json.load(config)
            except json.JSONDecodeError:
                print("Il file config.json è vuoto o non contiene un JSON valido.\nRiscaricandolo...")
                # TODO Scarica il file .json dalla repo

            if "token" not in data:
                print("In config.json there isn't 'token' key.\nAdding it...")
                data = {
                    "token": "PASTE_YOUR_TOKEN_HERE"
                }

                json.dump(data, config)
                config.truncate()

            config.close()


    except FileNotFoundError:
        print(f"The config file doesn't exist.\nGenerating it...")
        # TODO Scarica file dalla repo

    return data["token"]
