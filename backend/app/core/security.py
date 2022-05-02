from cryptography.fernet import Fernet
from app.config.settings import settings


def encrypt_password(password: str) -> str:
    return Fernet(settings.SECRET_KEY.encode()).encrypt(password.encode()).decode()


def decrypt_password(encrypted_password: str) -> str:
    return Fernet(settings.SECRET_KEY.encode()).decrypt(encrypted_password.encode()).decode()
