from pydantic import BaseModel as PydanticBaseModel, Extra, validator


class BaseModel(PydanticBaseModel):
    class Config:
        extra = Extra.forbid
        validate_assignment = True
