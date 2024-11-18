from aiogram import types


async def help_callback(callback_query: types.CallbackQuery):
    """Handles the help button."""
    help_text = (
        "'SecureTalk' bot allows you to securely communicate using encryption.\n"
        "Use 'Start Conversation' to begin a secure chat.\n"
        "For further assistance, contact support."
    )
    await callback_query.message.answer(help_text)
    await callback_query.answer()


async def generate_keypair_callback(callback_query: types.CallbackQuery):
    """Handles the start conversation button."""
    await callback_query.message.answer(
        "🔑 Generating your key pair...\nFeature coming soon!",
    )
    await callback_query.answer()


async def start_conversation_callback(callback_query: types.CallbackQuery):
    """Handles the start conversation button."""
    await callback_query.message.answer("Starting a secure conversation... 🔐")
    await callback_query.answer()
