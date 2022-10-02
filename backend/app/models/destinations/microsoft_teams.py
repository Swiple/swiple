from pydantic.fields import Field

from app.models.base_model import BaseModel
from typing import Literal
from app import constants as c
from app.models.types import EncryptedStr


class MicrosoftTeamsDestination(BaseModel):
    class Config:
        title = c.MICROSOFT_TEAMS
    destination_type: Literal[c.MICROSOFT_TEAMS]
    webhook: EncryptedStr = Field(placeholder="https://swiple.webhook.office.com/webhookb2/...@.../IncomingWebhook/.../...")


class MicrosoftTeamsDetails(BaseModel):
    class Config:
        title = f"{c.MICROSOFT_TEAMS}Details"
    destination_type: Literal[c.MICROSOFT_TEAMS]
    notify_on: Literal["all", "failure", "success"]


class MicrosoftTeams(MicrosoftTeamsDestination, MicrosoftTeamsDetails):
    pass
