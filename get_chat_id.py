"""Utility script to list chat IDs for a Telegram bot.

Run this script after setting the TELEGRAM_BOT_TOKEN environment variable.
It will query ``getUpdates`` and print any group or supergroup chat IDs
found in the response.
"""

from __future__ import annotations

import os
import requests


def get_chat_ids(token: str) -> list[dict[str, int | str]]:
    """Return a list of group names and chat IDs from the bot updates."""
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url, timeout=30)
    data = response.json()
    groups = set()

    for result in data.get("result", []):
        chat = (
            result.get("message", {}).get("chat")
            or result.get("my_chat_member", {}).get("chat")
        )
        if chat and chat.get("type") in ("group", "supergroup"):
            groups.add((chat.get("title"), chat.get("id")))

    return [{"group_name": name, "chat_id": chat_id} for name, chat_id in groups]


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN environment variable")

    for info in get_chat_ids(token):
        print(info)


if __name__ == "__main__":  # pragma: no cover - manual utility
    main()

