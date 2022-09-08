from pydantic import BaseModel as PydanticBaseModel, Extra

from app.models.types import EncryptedStr
from app import constants as c


class BaseModel(PydanticBaseModel):
    class Config:
        extra = Extra.forbid
        validate_assignment = True
        json_encoders = {
            EncryptedStr: lambda _: c.SECRET_MASK
        }
