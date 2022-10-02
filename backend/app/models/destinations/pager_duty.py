from app.models.base_model import BaseModel
from pydantic import Field
from typing import Optional, Literal
from app import constants as c
from app.models.types import EncryptedStr


class PagerDutyDestination(BaseModel):
    class Config:
        title = c.PAGER_DUTY

    destination_type: Literal[c.PAGER_DUTY]
    integration_key: EncryptedStr
    api_key: EncryptedStr
    region: Optional[Literal["us", "eu"]] = Field(default="us", description="'us' or 'eu'. Defaults to 'us'")
    component: Optional[str] = Field(default='Swiple', description="Component of the source machine that is responsible for the event, for example `Swiple`. Defaults to `Swiple`")


class PagerDutyDetails(BaseModel):
    destination_type: Literal[c.PAGER_DUTY]
    notify_on: Literal["all", "failure", "success"]


class PagerDuty(PagerDutyDestination, PagerDutyDetails):
    pass
