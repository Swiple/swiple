from typing import TYPE_CHECKING, Any, Dict

from cryptography.fernet import InvalidToken
from pydantic.utils import update_not_none
from pydantic.validators import str_validator

from app.core import security

if TYPE_CHECKING:
    from pydantic import BaseModel
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

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, EncryptedStr) and self.get_decrypted_value() == other.get_decrypted_value()

    def get_decrypted_value(self) -> str:
        return security.decrypt_password(self)


class EncryptedStrSetterMixin:
    """
    Mixin to overload the setter method of Pydantic models
    using an `EncryptedStr` field.

    By default, when setting an attribute like this:

    ```py
    my_object.encrypted_value = "VALUE"
    ```

    Pydantic will just store it as a plain string without
    respecting the type we gave on the model class.

    We overload this behavior by checking if the field
    we are currently setting has the `EncryptedStr` type.
    If it does, we take care of instantiating a proper `EncryptedStr`
    instance so our string is correctly encrypted.
    """
    def __setattr__(self: "BaseModel", name: str, value: Any) -> None:
        field = self.__fields__.get(name)
        if field and field.type_ == EncryptedStr:
            return super().__setattr__(name, EncryptedStr(value))
        return super().__setattr__(name, value)
