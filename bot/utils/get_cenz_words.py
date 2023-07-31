import json
import os


def get_cenz_data() -> set:
    path = os.path.join(os.getcwd(), r"bot\utils\cenz.json")

    with open(path, "r", encoding="utf-8") as file:
        return set(json.load(file))
