import json
import os

MEMORY_FILE = "data/memory.json"


def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(
            MEMORY_FILE,
            "r"
        ) as f:

            return json.load(f)

    return {}


def save_memory(memory):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        MEMORY_FILE,
        "w"
    ) as f:

        json.dump(
            memory,
            f,
            indent=4
        )


def remember(
    memory,
    key,
    value
):

    memory[key] = value

    save_memory(memory)


def recall(
    memory,
    key
):

    return memory.get(key)