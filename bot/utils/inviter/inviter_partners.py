import json

from bot.core.redis_client import get_redis_client

redis_client = get_redis_client()


async def get_inviter_partners(inviter_id: int):
    conversations = await redis_client.smembers(f"inviter_conversations:{inviter_id}")
    invitees = []

    if conversations:
        for conversation in conversations:
            secure_id, invitee_id = conversation.split(":")
            invitee_data_json = await redis_client.get(
                f"conversation_invitee:{secure_id}",
            )
            if invitee_data_json:
                invitees.append(json.loads(invitee_data_json))
            else:
                # Cleaning up expired conversations using TTL parameter embedded into
                # 'conversation_invitee:{secure_id}' (from store_invitee.py)
                await redis_client.srem(
                    f"inviter_conversations:{inviter_id}",
                    f"{secure_id}:{invitee_id}",
                )
    return invitees
