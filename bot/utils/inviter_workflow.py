from bot.keys.rsa_key import encrypt_private_key
from bot.keys.rsa_key import generate_rsa_keypair
from bot.keys.rsa_store import rsa_store


async def initialize_inviter_workflow(inviter_id: int):
    """Generates and stores RSA keypair for an inviter."""
    private_pem, public_pem = await generate_rsa_keypair()
    encrypted_private_key = await encrypt_private_key(
        private_pem,
        f"passphrase_for_{inviter_id}",
    )
    await rsa_store(inviter_id, encrypted_private_key, public_pem)
