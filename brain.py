import requests


def ask_ollama(prompt):

    try:

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        if response.status_code != 200:

            print(
                "OLLAMA DEBUG:",
                response.text
            )

            return (
                "My brain is offline."
            )

        data = response.json()

        return data.get(
            "response",
            ""
        )

    except Exception as e:

        print(
            "OLLAMA ERROR:",
            e
        )

        return (
            "My brain is offline."
        )