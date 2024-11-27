import requests
from config import CLAUDE_API_KEY, CLAUDE_API_URL


def connect_to_claude_api(content: str, prefs: str, word_limit: int):
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"""
        Create two concise summaries of the following newsletter content:

        1. General summary: {content}

        2. Personalized summary considering user's preferences: {prefs}.

        Please keep both summaries under {word_limit} words.
        """,
        "max_tokens": word_limit,
        "stop_sequences": ["\n"]
    }

    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Błąd komunikacji z API: {response.status_code}, {response.text}")

    return response.json()