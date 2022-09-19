from typing import TYPE_CHECKING, Any, Dict

from cryptography.fernet import InvalidToken
from pydantic.utils import update_not_none
from pydantic.validators import str_validator
from great_expectations.data_context import util
from app.core import security
from app import constants as c

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class EncryptedStr(str):
    """Representation of an encrypted string."""

    def __new__(cls, value):
        """
        Create a string object from the given value.

        We try to decrypt it to check if it's already an encrypted value,
        e.g. if it comes from the database. If it is, we just set it as it.

        Otherwise, we encrypt it immediately.
        """
        try:
            security.decrypt_password(value)
            return super(EncryptedStr, cls).__new__(cls, value)
        except InvalidToken:
            return super(EncryptedStr, cls).__new__(cls, security.encrypt_password(value))

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(
            field_schema,
            type="string",
            writeOnly=True,
            format="password",
        )

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> 'EncryptedStr':
        if isinstance(value, cls):
            return value
        value = str_validator(value)
        return cls(value)

    def __repr__(self) -> str:
        return f"EncryptedStr('**********')"

    def __str__(self) -> str:
        return c.SECRET_MASK if self.get_decrypted_value() else ""

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, EncryptedStr) and self.get_decrypted_value() == other.get_decrypted_value()

    def get_decrypted_value(self) -> str:
        decrypted_value: str = security.decrypt_password(self)
        # if the decrypted_value matches the regex of a secrets provider,
        # e.g. AWS Secrets Manager, GCP Secret Manager, Azure Key Vault
        # get secret value from provider
        print(util.substitute_value_from_secret_store(decrypted_value))
        return util.substitute_value_from_secret_store(decrypted_value)
