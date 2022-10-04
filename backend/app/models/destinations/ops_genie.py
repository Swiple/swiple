from app.models.base_model import BaseModel
from typing import Literal
from app import constants as c
from app.models.types import EncryptedStr


class OpsGenieDestination(BaseModel):
    class Config:
        title = c.OPS_GENIE
    destination_type: Literal[c.OPS_GENIE]
    api_key: EncryptedStr


class OpsGenieDetails(BaseModel):
    class Config:
        title = c.OPS_GENIE
    destination_type: Literal[c.OPS_GENIE]
    notify_on: Literal["all", "failure", "success"]
    priority: Literal["P1", "P2", "P3", "P4", "P5"]


class OpsGenie(OpsGenieDestination, OpsGenieDetails):
    pass
