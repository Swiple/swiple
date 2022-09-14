import uuid
from pydantic import BaseModel as PydanticBaseModel, Extra, Field

from app.models.types import EncryptedStr
from app import constants as c
from app import utils


class BaseModel(PydanticBaseModel):
    class Config:
        extra = Extra.forbid
        validate_assignment = True
        json_encoders = {
            EncryptedStr: lambda _: c.SECRET_MASK
        }


def generate_key() -> str:
    return str(uuid.uuid4)


class KeyModel(PydanticBaseModel):
    key: str = Field(default_factory=generate_key)


class CreateUpdateDateModel(PydanticBaseModel):
    create_date: str = Field(default_factory=utils.current_time)
    modified_date: str = Field(default_factory=utils.current_time)
