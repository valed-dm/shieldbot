from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from bot.keys.aes.sym_key import retrieve_symmetric_key
from bot.keys.encrypt_decrypt import decrypt_message_with_aes

if TYPE_CHECKING:
    from bot.callbacks.data.callback_controller import CallbackController


async def decrypt_text(callback: CallbackController) -> tuple[str, Any]:
    symmetric_key = retrieve_symmetric_key(conversation_id=callback.secure_id)
    iv_ciphertext = bytes.fromhex(callback.callback_data)

    decrypted_text = await decrypt_message_with_aes(
        key=symmetric_key,
        iv_ciphertext=iv_ciphertext,
    )

    return (
        decrypted_text,
        callback.inviter_username
        if callback.role == "invitee"
        else callback.invitee_username,
    )
