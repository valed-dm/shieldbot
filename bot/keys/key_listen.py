import json
import logging

from bot.core.redis_client import get_redis_client
from bot.keys.key_status import notify_key_received
from bot.keys.rsa_key import decrypt_private_key
from bot.keys.rsa_store import sync_retrieve_private_key
from bot.keys.sym_key import decrypt_symmetric_key_with_rsa
from bot.keys.sym_key import save_symmetric_key

logger = logging.getLogger("SYM_LISTENER")
redis_client = get_redis_client()


async def listen_for_sym_notifications(inviter_id: int):
    """Listens for notifications, decrypts and store the symmetric key."""
    channel_name = f"conversation:notifications:{inviter_id}"
    redis_sub = redis_client.pubsub()
    await redis_sub.subscribe(channel_name)

    async for message in redis_sub.listen():
        if message["type"] == "message":
            d = json.loads(message["data"])
            status = d["event"]

            if status == "key_ready":
                secure_id = d.get("data")
                # Fetch the encrypted symmetric key from Redis
                encrypted_symmetric_key_hex = await redis_client.get(
                    f"{secure_id}:encrypted_key",
                )
                if encrypted_symmetric_key_hex:
                    encrypted_symmetric_key = bytes.fromhex(encrypted_symmetric_key_hex)

                    inviter_private_pem_encrypted = sync_retrieve_private_key(
                        inviter_id,
                    )

                    passphrase = f"passphrase_for_{inviter_id}"
                    inviter_private_pem = await decrypt_private_key(
                        inviter_private_pem_encrypted,
                        passphrase,
                    )

                    # Decrypt the symmetric key using the private key
                    symmetric_key = await decrypt_symmetric_key_with_rsa(
                        private_key_pem=inviter_private_pem,
                        encrypted_key=encrypted_symmetric_key,
                    )

                    # Stores the symmetric key in inviter's Keychain/Keystore
                    save_symmetric_key(
                        conversation_id=secure_id,
                        symmetric_key=symmetric_key,
                    )

                    msg = (
                        f"Inviter's {inviter_id} symmetric key "
                        f"for {secure_id} stored successfully!"
                    )
                    logger.info(msg)

                    await notify_key_received(inviter_id, secure_id)
