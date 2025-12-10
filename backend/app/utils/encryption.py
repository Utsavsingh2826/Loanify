"""Encryption utilities for sensitive data."""
from cryptography.fernet import Fernet
from app.config import settings
import base64
import hashlib


def get_encryption_key() -> bytes:
    """Get encryption key from secret."""
    # Derive a Fernet key from the secret key
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


cipher = Fernet(get_encryption_key())


def encrypt_data(data: str) -> str:
    """Encrypt sensitive data."""
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data."""
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()


def encrypt_sensitive_fields(data: dict, fields: list) -> dict:
    """Encrypt specific fields in a dictionary."""
    encrypted_data = data.copy()
    for field in fields:
        if field in encrypted_data and encrypted_data[field]:
            encrypted_data[field] = encrypt_data(str(encrypted_data[field]))
    return encrypted_data


def decrypt_sensitive_fields(data: dict, fields: list) -> dict:
    """Decrypt specific fields in a dictionary."""
    decrypted_data = data.copy()
    for field in fields:
        if field in decrypted_data and decrypted_data[field]:
            try:
                decrypted_data[field] = decrypt_data(decrypted_data[field])
            except Exception:
                pass  # Field might not be encrypted
    return decrypted_data


