import json

from bot.core.redis_client import get_redis_client
from bot.utils.user_data_resolver import UserDataResolver

TTL = 3600

redis_client = get_redis_client()


async def store_invitee(secure_id: str, invitee: UserDataResolver):
    invitee_data = {
        "secure_id": secure_id,
        "invitee_id": invitee.id,
        "username": invitee.username,
        "first_name": invitee.first_name,
        "last_name": invitee.last_name,
    }
    await redis_client.setex(
        f"conversation_invitee:{secure_id}",
        TTL,
        json.dumps(invitee_data),
    )
