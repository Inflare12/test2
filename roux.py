from brain import ask_ollama
from memory import *
from personality import ROUX_PERSONALITY
from safety import *
import time
import gc
from emotion import *
from voice import listen
from speak import speak
def search_knowledge(query):
    return ""
# ==========================
# LOAD MEMORY
# ==========================

memory = load_memory()

try:
    emotions = load_emotions()
except:
    emotions = {
        "happy": 50,
        "sad": 0,
        "worried": 0,
        "excited": 0
    }

# ==========================
# STARTUP
# ==========================

print("ROUX AI v1.0")
print("Voice Mode Active")
print("Wake Word: Rox Fox")

speak("Hello. I am Roux.")

# ==========================
# MAIN LOOP
# ==========================

while True:

# ==========================
# INPUT (VOICE + TERMINAL)
# ==========================

    print("\n--------------------------------")
    print("Type a message and press Enter.")
    print("Or press Enter without typing to use voice.")
    print("--------------------------------")

    try:
        typed = input("You (type or press Enter for voice): ").strip()

        if typed:
            user = typed
        else:
            print("Listening...")
            user = listen()

    except Exception as e:
        print("Input Error:", e)
        continue

    if not user:
        continue

    user = user.strip()

    print("\nYou:", user)
    # ==========================
    # EXIT
    # ==========================

    if user.lower() in [
        "exit",
        "quit",
        "bye",
        "goodbye"
    ]:

        name = recall(memory, "name")

        if name:
            reply = f"Goodbye {name}."
        else:
            reply = "Goodbye."

        print("\nRoux:", reply)

        speak(reply)

        gc.collect()
        time.sleep(1)

        break

    # ==========================
    # SAFETY
    # ==========================

    if check_emergency(user):

        reply = (
            "That sounds serious. "
            "Please contact emergency services, "
            "a doctor, or a trusted adult immediately."
        )

        print("\nRoux:", reply)

        speak(reply)

        continue

    # ==========================
    # LEARN NAME
    # ==========================

    if "my name is" in user.lower():

        name = (
            user.lower()
            .split("my name is")[-1]
            .strip()
        )

        remember(
            memory,
            "name",
            name
        )

        reply = (
            f"Nice to meet you {name}. "
            f"I will remember that."
        )

        print("\nRoux:", reply)

        speak(reply)

        continue

    # ==========================
    # RECALL NAME
    # ==========================

    if (
        "what is my name" in user.lower()
        or
        "what's my name" in user.lower()
    ):

        name = recall(
            memory,
            "name"
        )

        if name:
            reply = f"Your name is {name}."
        else:
            reply = (
                "I do not know your name yet."
            )

        print("\nRoux:", reply)

        speak(reply)

        continue

    # ==========================
    # EMOTION SYSTEM
    # ==========================

    try:

        emotions = update_emotions(
            user,
            emotions
        )

        for key in emotions:
            emotions[key] *= 0.95

        mood = get_mood(
            emotions
        )

    except Exception as e:

        print(
            "Emotion Error:",
            e
        )

        mood = "neutral"

    print(
        "\nEmotion:",
        mood
    )

    # ==========================
    # SEMANTIC SEARCH
    # ==========================

    try:

        knowledge = search_knowledge(
            user
        )

        print(
            "\n===================="
        )

        print(
            "KNOWLEDGE FOUND:"
        )

        print(
            knowledge[:1000]
        )

        print(
            "====================\n"
        )

    except Exception as e:

        print(
            "Search Error:",
            e
        )

        knowledge = (
            "No knowledge found."
        )

    # ==========================
    # BUILD PROMPT
    # ==========================

    prompt = f"""
{ROUX_PERSONALITY}

You are Roux.

Facts:

- You are Roux.
- Pronounced Rox.
- Created by Kunj.
- You are an AI robot companion.
- Never say you are Qwen.
- Never say you are created by Alibaba.
- Use memory.
- Use health knowledge when useful.
- Speak naturally.
- Keep responses short.

Current Mood:
{mood}

Memory:
{memory}

Knowledge:
{knowledge}

User:
{user}

Roux:
"""

    # ==========================
    # OLLAMA
    # ==========================

    try:

        reply = ask_ollama(
            prompt
        )
        reply = str(reply).strip()

        reply = reply.replace(
            "Roux:",
            ""
        )

        reply = reply.replace(
            "Assistant:",
            ""
        )
        if not reply:

            reply = (
                "Sorry. "
                "My brain is not responding."
            )

    except Exception as e:

        print(
            "Brain Error:",
            e
        )

        reply = (
            "Sorry. "
            "My brain is not responding."
        )

    # ==========================
    # CLEAN OUTPUT
    # ==========================

    reply = str(reply).strip()

    if len(reply) > 1000:

        reply = reply[:1000]

    # ==========================
    # SPEAK
    # ==========================

    print(
        "\nRoux:",
        reply
    )

    try:

        speak(reply)

    except Exception as e:

        print(
            "Speech Error:",
            e
        )