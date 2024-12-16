import pytest

from bot.keys.aes.sym_key import decrypt_symmetric_key_with_rsa
from bot.keys.aes.sym_key import encrypt_symmetric_key_with_rsa
from bot.keys.aes.sym_key import generate_symmetric_key
from bot.keys.rsa.rsa_key import generate_rsa_keypair


async def test_full_key_exchange_workflow():
    private_pem, public_pem = await generate_rsa_keypair()
    symmetric_key = generate_symmetric_key()
    encrypted_key = await encrypt_symmetric_key_with_rsa(public_pem, symmetric_key)
    decrypted_key = await decrypt_symmetric_key_with_rsa(private_pem, encrypted_key)

    if symmetric_key != decrypted_key:
        pytest.fail(" test_full_key_exchange_workflow failed!")
