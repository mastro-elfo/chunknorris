"""Encrypt and decrypt messages"""

import os
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e

from cryptography.exceptions import InternalError
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
ITERATIONS: int = 1000
ITERATIONS_SIZE: int = 4
SALT_SIZE: int = 16


class DecryptionError(Exception):
    """Exception raised during decryption"""


def _derive_key(password: bytes, salt: bytes, iterations: int) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend,
    )
    return b64e(kdf.derive(password))


def encrypt(message: bytes, password: str, iterations: int = ITERATIONS) -> bytes:
    """Encrypt message with the given password"""
    salt = os.urandom(SALT_SIZE)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b"%b%b%b"
        % (
            salt,
            iterations.to_bytes(ITERATIONS_SIZE, "big"),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def decrypt(token: bytes, password: str) -> bytes:
    """Decrypt token with the given password"""

    try:
        decoded = b64d(token)
        salt, iterations, token = (
            decoded[:SALT_SIZE],
            decoded[SALT_SIZE : SALT_SIZE + ITERATIONS_SIZE],
            b64e(decoded[20:]),
        )
        iterations = int.from_bytes(iterations, "big")
        key = _derive_key(password.encode(), salt, iterations)
        return Fernet(key).decrypt(token)
    except InvalidToken as error:
        raise DecryptionError("Invalid token or wrong password") from error
    except InternalError as error:
        raise DecryptionError(
            "Internal error, file il probably not encrypted"
        ) from error
