import os
from typing import cast

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes, PublicKeyTypes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

from .constants import PRIVATE_KEY, PUBLIC_KEY

env_private_key: str = os.getenv("PRIVATE_KEY", PRIVATE_KEY)
env_public_key: str = os.getenv("PUBLIC_KEY", PUBLIC_KEY)


def env_keys(env_private_key: str, env_public_key: str) -> tuple:
    env_private_key_bytes: bytes = env_private_key.replace("\\n", "\n").encode()
    env_public_key_bytes: bytes = env_public_key.replace("\\n", "\n").encode()
    return env_private_key_bytes, env_public_key_bytes


env_private_key_bytes, env_public_key_bytes = env_keys(env_private_key, env_public_key)

private_key_var: PrivateKeyTypes = load_pem_private_key(env_private_key_bytes, password=None, backend=default_backend())
public_key_var: PublicKeyTypes = load_pem_public_key(env_public_key_bytes, backend=default_backend())


def public_key() -> ed25519.Ed25519PublicKey:
    """
    Returns the public key to verify the JWT.
    """
    return cast(ed25519.Ed25519PublicKey, public_key_var)


def private_key() -> ed25519.Ed25519PrivateKey:
    """
    Returns the private key to sign the JWT.
    """
    return cast(ed25519.Ed25519PrivateKey, private_key_var)
