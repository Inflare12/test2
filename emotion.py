import json
import os

EMOTION_FILE = "emotion.json"

DEFAULT_EMOTIONS = {
    "happy": 50,
    "sad": 0,
    "worried": 0,
    "excited": 0
}


def load_emotions():

    if not os.path.exists(EMOTION_FILE):

        save_emotions(DEFAULT_EMOTIONS)

        return DEFAULT_EMOTIONS.copy()

    with open(EMOTION_FILE, "r") as f:

        return json.load(f)


def save_emotions(emotions):

    with open(EMOTION_FILE, "w") as f:

        json.dump(emotions, f, indent=4)


def update_emotions(user_text, emotions):

    text = user_text.lower()

    happy_words = [
        "happy",
        "great",
        "awesome",
        "won",
        "passed",
        "success",
        "good"
    ]

    sad_words = [
        "sad",
        "cry",
        "depressed",
        "failed",
        "lost",
        "hurt"
    ]

    worried_words = [
        "sick",
        "hospital",
        "injury",
        "bleeding",
        "pain",
        "worried"
    ]

    excited_words = [
        "robot",
        "robotics",
        "ai",
        "project",
        "build",
        "create"
    ]

    for word in happy_words:
        if word in text:
            emotions["happy"] += 10

    for word in sad_words:
        if word in text:
            emotions["sad"] += 10

    for word in worried_words:
        if word in text:
            emotions["worried"] += 10

    for word in excited_words:
        if word in text:
            emotions["excited"] += 10

    for key in emotions:

        if emotions[key] > 100:
            emotions[key] = 100

        if emotions[key] < 0:
            emotions[key] = 0

    save_emotions(emotions)

    return emotions


def get_mood(emotions):

    highest = max(emotions, key=emotions.get)

    return highest

