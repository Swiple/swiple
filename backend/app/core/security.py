from app.core import exceptions
from app.settings import settings
try:
    import botocore.exceptions
except ImportError:
    botocore = None
from cryptography.fernet import Fernet
from great_expectations.data_context import util


def encrypt_password(password: str) -> str:
    return Fernet(settings.SECRET_KEY.encode()).encrypt(password.encode()).decode()


def decrypt_password(encrypted_password: str) -> str:
    return Fernet(settings.SECRET_KEY.encode()).decrypt(encrypted_password.encode()).decode()


def substitute_value_from_secret_store(value: str):
    """Retrieves Secrets from AWS Secrets Manager, GCP Secret Manager & Azure Key Vault"""
    try:
        value: str = util.substitute_value_from_secret_store(value)
    except ValueError:
        exception_msg = "The format of the secret provided appears to be incorrect. Please review " \
                        "https://swiple.io/docs/how-to-guides/secrets-manager#aws-secrets-manager-setup for how " \
                        "secrets should be formatted."

        raise exceptions.SecretClientError(Exception(exception_msg))
    except ImportError as e:
        raise exceptions.SecretsModuleNotFoundError(e.msg)
    except KeyError as e:
        raise exceptions.SecretsKeyError(e.__str__())
    except botocore.exceptions.ClientError as e:
        raise exceptions.SecretClientError(e)
    except botocore.exceptions.NoCredentialsError as e:
        raise exceptions.NoCredentialsError(e)
    return value
