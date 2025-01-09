"""Callbacks registration module."""

from functools import partial

from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from bot.callbacks.abort_button_click import on_abort_button_click
from bot.callbacks.decrypt_button_click import on_decrypt_button_click
from bot.callbacks.invitee.confirm_button_click import on_confirm_button_click
from bot.callbacks.invitee.decline_button_click import on_decline_button_click
from bot.callbacks.invitee.invitee_button_input import on_invitee_button_click
from bot.callbacks.invitee.invitee_manual_input import on_manual_invitee_input
from bot.callbacks.invitee.invitees_reset import on_reset_invitees
from bot.callbacks.inviter.cancel_button_click import on_cancel_button_click
from bot.commands.help import help_callback
from bot.commands.securetalk import on_prepare_secure_talk
from bot.commands.settings import on_settings

CALLBACK_HELP = "help"
CALLBACK_SETTINGS = "settings"
CALLBACK_PREPARE_SECURETALK = "ir:prepare:"
CALLBACK_MANUAL_INVITEE_INPUT = "ie:input:"
CALLBACK_SAVED_INVITEE_INPUT = "ir:invite:"
CALLBACK_ACCEPT_INVITATION = "ie:accept:"
CALLBACK_DECLINE_INVITATION = "ie:decline:"
CALLBACK_CANCEL_INVITATION = "ir:cancel:"
CALLBACK_RESET_INVITEES = "ir:reset:"
CALLBACK_INVITER_DECRYPT = "ir:decrypt:"
CALLBACK_INVITEE_DECRYPT = "ie:decrypt:"
CALLBACK_INVITER_ABORT = "ir:abort:"
CALLBACK_INVITEE_ABORT = "ie:abort:"

router = Router(name=__name__)


class CallbackFilter(Filter):
    """
    Custom filter for callback queries based on matching specific callback data.

    This filter is designed to compare the callback data in a query with a
    predefined text value (`my_text`). It is useful for handling specific
    callback actions in Telegram bots.

    :param my_text: The callback data to match against.
    :type my_text: str
    """

    def __init__(self, my_text: str) -> None:
        """
        Initializes the filter with the specified callback data to match.

        :param my_text: The callback data to be matched.
        """
        self.my_text = my_text

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        """
        Compares the callback data in the query with the specified text.

        :param callback_query: The callback query object to evaluate.
        :type callback_query: CallbackQuery
        :return: True if the callback data matches `my_text`, False otherwise.
        :rtype: bool
        """
        return callback_query.data == self.my_text


router.callback_query.register(
    help_callback,
    CallbackFilter(CALLBACK_HELP),
)
router.callback_query.register(
    on_settings,
    CallbackFilter(CALLBACK_SETTINGS),
)
router.callback_query.register(
    on_reset_invitees,
    CallbackFilter(CALLBACK_RESET_INVITEES),
)
router.callback_query.register(
    on_prepare_secure_talk,
    CallbackFilter(CALLBACK_PREPARE_SECURETALK),
)
router.callback_query.register(
    on_manual_invitee_input,
    CallbackFilter(CALLBACK_MANUAL_INVITEE_INPUT),
)
router.callback_query.register(
    on_invitee_button_click,
    lambda c: c.data and c.data.startswith(CALLBACK_SAVED_INVITEE_INPUT),
)
router.callback_query.register(
    on_confirm_button_click,
    lambda c: c.data and c.data.startswith(CALLBACK_ACCEPT_INVITATION),
)
router.callback_query.register(
    on_decline_button_click,
    lambda c: c.data and c.data.startswith(CALLBACK_DECLINE_INVITATION),
)
router.callback_query.register(
    on_cancel_button_click,
    lambda c: c.data and c.data.startswith(CALLBACK_CANCEL_INVITATION),
)
router.callback_query.register(
    partial(on_decrypt_button_click, expected_prefix="ir:decrypt:"),
    lambda c: c.data and c.data.startswith(CALLBACK_INVITER_DECRYPT),
)
router.callback_query.register(
    partial(on_decrypt_button_click, expected_prefix="ie:decrypt:"),
    lambda c: c.data and c.data.startswith(CALLBACK_INVITEE_DECRYPT),
)
router.callback_query.register(
    partial(on_abort_button_click, expected_prefix="ir:abort:"),
    lambda c: c.data and c.data.startswith(CALLBACK_INVITER_ABORT),
)
router.callback_query.register(
    partial(on_abort_button_click, expected_prefix="ie:abort:"),
    lambda c: c.data and c.data.startswith(CALLBACK_INVITEE_ABORT),
)
