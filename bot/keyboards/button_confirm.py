import os

from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

LOGO = os.getenv("LOGO")


def confirm_button(role_action_id: str):
    """Prepare 'Confirm' button to be used in the invitee's
    SecureTalk confirmation Keyboard"""
    button = InlineKeyboardButton(
        text=f"✅{LOGO}",
        callback_data=role_action_id,
    )
    return button
