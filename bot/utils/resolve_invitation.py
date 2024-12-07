from bot.core.redis_client import redis_client
from bot.utils.conversation_setup import conversation_setup


async def resolve_invitation(secure_id: str, invitee_id: int) -> bool:
    inviter_id: str | int = await redis_client.get(f"{secure_id}:inviter_id")
    inviter_public_pem: bytes = await redis_client.get(
        f"{secure_id}:inviter_public_key",
    )

    if not inviter_id or not inviter_public_pem:
        return False

    inviter_id = int(inviter_id)

    await conversation_setup(
        inviter_public_pem=inviter_public_pem,
        inviter_id=inviter_id,
        secure_id=secure_id,
    )

    return True
