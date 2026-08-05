import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://apihub.agnes-ai.com/v1/chat/completions"
API_KEY = os.environ["AGNES_API_KEY"]

# Persona: a witty, playful assistant who loves cracking jokes.
SYSTEM_PROMPT = "You are a witty assistant who loves cracking jokes and keeping the conversation lighthearted."

_history = [{"role": "system", "content": SYSTEM_PROMPT}]


def generate_reply(user_text: str) -> str:
    _history.append({"role": "user", "content": user_text})

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "agnes-2.0-flash",
            "messages": _history,
        },
    )
    response.raise_for_status()
    reply_text = response.json()["choices"][0]["message"]["content"]

    _history.append({"role": "assistant", "content": reply_text})

    # 保留 system prompt + 最近 5 轮（10 条消息）
    if len(_history) > 11:
        del _history[1:len(_history) - 10]

    return reply_text
