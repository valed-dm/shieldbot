from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


async def menu_command(message: types.Message):
    """Display the main menu with inline keyboard buttons."""
    # Define buttons
    buttons = [
        [
            InlineKeyboardButton(
                text="Start Conversation",
                callback_data="start_conversation",
            ),
        ],
        [InlineKeyboardButton(text="Help", callback_data="help")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        "Welcome to ShieldBot! Choose an option:",
        reply_markup=keyboard,
    )


async def start_conversation_callback(callback_query: types.CallbackQuery):
    """Handles the start conversation button."""
    await callback_query.message.answer("Starting a secure conversation... 🔐")
    await callback_query.answer()  # Acknowledge the callback


async def help_callback(callback_query: types.CallbackQuery):
    """Handles the help button."""
    help_text = (
        "ShieldBot allows you to securely communicate using encryption.\n"
        "Use 'Start Conversation' to begin a secure chat.\n"
        "For further assistance, contact support."
    )
    await callback_query.message.answer(help_text)
    await callback_query.answer()  # Acknowledge the callback
