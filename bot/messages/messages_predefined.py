import os

from dotenv import load_dotenv

load_dotenv()

LOGO = os.getenv("LOGO")


def invalid_format():
    return "Telegram invalid username (must start with '@') format."


def unexpected_err_msg(username: str, error: Exception) -> str:
    return (
        f"{LOGO} error resolving partner ID for {username!r}: {error!r}. "
        f"Please try again later."
    )
