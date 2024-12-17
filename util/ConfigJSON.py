import json
import re


def token():
    try:
        with open("config.json", "r+") as config:
            data = json.load(config)
    except Exception as e:
        print(e)

    return data["token"]

def remove_trailing_commas(json_str):
    # Remove any commas that are followed by closing brackets or braces
    json_str = re.sub(r',\s*(]|\})', r'\1', json_str)
    return json_str


def format_users(data):
    #?remove user without username field
    for user in data["users"]:
        if "username" not in user:
            data["users"].remove(user)
        elif user["username"] == "":
            data["users"].remove(user)

    #?set default value for field foreach user
    for user in data["users"]:
        if "lang" not in user:
            user["lang"] = "en_GB"
        if "debugMode" not in user:
            user["debugMode"] = False
        if "is_op" not in user:
            user["is_op"] = False
    return data

def checkConfigJSON():
    try:

        with open("config.json", "r+") as config:

            try:
                raw_data = remove_trailing_commas(config.read())
                dataLoaded = json.loads(raw_data)


                if "token" not in dataLoaded:
                    dataTemp = {"token": "PASTE_YOUR_TOKEN_HERE"}
                    dataLoaded = dataTemp.update(dataLoaded)

                if "version" not in dataLoaded:
                    dataTemp = {"version": "v1.0"}
                    dataLoaded.update(dataTemp)

                dataLoaded = format_users(dataLoaded)

                config.seek(0)
                json.dump(dataLoaded, config, indent=4)
                config.truncate()


            except json.JSONDecodeError:
                pass
                # TODO Scarica il file .json dalla repo

    except FileNotFoundError:
        print(f"The config file doesn't exist.\nGenerating it...")
        # TODO Scarica file dalla repo