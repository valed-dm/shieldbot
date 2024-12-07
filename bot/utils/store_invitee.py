import json

from bot.core.redis_client import redis_client

TTL = 3600


async def store_invitee(
    secure_id: str,
    partner_id: int,
    partner_username: str,
    partner_first_name: str,
    partner_last_name: str,
):
    invitee_data = {
        "invitee_id": partner_id,
        "username": partner_username,
        "first_name": partner_first_name,
        "last_name": partner_last_name,
    }
    await redis_client.setex(
        f"conversation_invitee:{secure_id}",
        TTL,
        json.dumps(invitee_data),
    )
