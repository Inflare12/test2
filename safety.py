EMERGENCY_WORDS = [
    "dying",
    "can't breathe",
    "heart attack",
    "stroke",
    "suicide",
    "unconscious",
    "help"
]

def check_emergency(text):

    text = text.lower()

    for word in EMERGENCY_WORDS:
        if word in text:
            return True

    return False