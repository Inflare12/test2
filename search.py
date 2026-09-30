import os
import re

KNOWLEDGE_FOLDER = "knowledge"

STOP_WORDS = {
    "i", "am", "is", "are", "was", "were",
    "the", "a", "an", "and", "or",
    "my", "me", "you", "your",
    "have", "has", "had",
    "got", "get", "getting",
    "with", "for", "from",
    "this", "that", "it",
    "in", "on", "at", "to",
    "of", "by"
}

SYNONYMS = {

    # injuries
    "bled": "bleeding",
    "bleed": "bleeding",
    "cut": "wound",
    "cuts": "wound",
    "hurt": "injury",
    "injured": "injury",

    # fatigue
    "weak": "fatigue",
    "tired": "fatigue",

    # digestion
    "poop": "stool",
    "pee": "urination",

    # heart
    "heartburn": "reflux",

    # rusty objects
    "rusty": "rusted",

    # breathing
    "breathless": "shortness",
}

def preprocess_query(query):

    words = re.findall(r"\b[a-z]+\b", query.lower())

    cleaned = []

    for word in words:

        if word in STOP_WORDS:
            continue

        if len(word) < 3:
            continue

        word = SYNONYMS.get(word, word)

        cleaned.append(word)

    return cleaned


def count_whole_word(word, text):

    matches = re.findall(
        r"\b" + re.escape(word) + r"\b",
        text
    )

    return len(matches)


def search_knowledge(query):

    query_words = preprocess_query(query)

    best_score = 0
    best_topic = None
    best_words = []

    for filename in os.listdir(KNOWLEDGE_FOLDER):

        filepath = os.path.join(
            KNOWLEDGE_FOLDER,
            filename
        )

        if not os.path.isfile(filepath):
            continue

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        topics = re.split(
            r"\n\s*\d+\.\s+",
            text
        )

        for topic in topics:

            if len(topic.strip()) < 100:
                continue

            topic_lower = topic.lower()

            score = 0
            matched_words = []

            for word in query_words:

                count = count_whole_word(
                    word,
                    topic_lower
                )

                if count > 0:

                    matched_words.append(word)

                    score += count * 10

                    # Extra bonus if found near top
                    if word in topic_lower[:500]:
                        score += 5

            if score > best_score:

                best_score = score
                best_topic = topic
                best_words = matched_words

    print("\n====================")
    print("SEARCH DEBUG")
    print("Query Words:", query_words)
    print("Score:", best_score)
    print("Matched:", best_words)
    print("====================")

    if best_topic:

        return best_topic[:4000]

    return "No relevant knowledge found."