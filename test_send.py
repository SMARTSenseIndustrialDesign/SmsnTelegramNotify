"""Simple CLI for sending a Telegram message."""

import argparse

from smsn_telegram.TelegramNotify import TelegramNotify


def main() -> None:
    """Parse arguments and send a message."""
    parser = argparse.ArgumentParser(description="Send a test Telegram message")
    parser.add_argument(
        "--token",
        help="Telegram bot token. If omitted, value from config will be used.",
    )
    parser.add_argument(
        "--chat-id",
        help="Chat ID of the destination channel. If omitted, value from config will be used.",
    )
    parser.add_argument(
        "--config-path",
        default="config.toml",
        help="Path to configuration file with default token/chat_id.",
    )
    parser.add_argument(
        "--message",
        default="Hello, World",
        help="Message to send",
    )
    args = parser.parse_args()

    tele_noti = TelegramNotify(
        token=args.token,
        chat_id=args.chat_id,
        config_path=args.config_path,
    )

    tele_noti.start_send_text(args.message)


if __name__ == "__main__":
    main()


