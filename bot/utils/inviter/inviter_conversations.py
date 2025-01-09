from bot.core.redis_client import get_redis_client

redis_client = get_redis_client()


async def store_inviter_conversations(
    secure_id: str,
    inviter_id: int,
    invitee_id: int,
) -> None:
    """Saves inviter's conversations data."""
    await redis_client.sadd(
        f"inviter_conversations:{inviter_id}",
        f"{secure_id}:{invitee_id}",
    )
