from __future__ import annotations

from bot.core.redis_client import get_redis_client
from bot.utils.conversation_setup import conversation_setup

redis_client = get_redis_client()


async def resolve_invitation(secure_id: str, invitee_id: int) -> tuple[int, str] | None:
    inviter_id = None
    inviter_username = None
    public_key_hex = None

    inviter_data = await redis_client.get(f"{secure_id}:inviter_data")
    if inviter_data:
        inviter_id, inviter_username, public_key_hex = inviter_data.split(":")

    if not inviter_id or not public_key_hex:
        return None

    inviter_id = int(inviter_id)
    inviter_public_pem = bytes.fromhex(public_key_hex)

    await conversation_setup(
        inviter_public_pem=inviter_public_pem,
        inviter_id=inviter_id,
        invitee_id=invitee_id,
        secure_id=secure_id,
    )

    return inviter_id, inviter_username
