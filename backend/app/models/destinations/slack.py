from pydantic.fields import Field

from app.models.base_model import BaseModel
from typing import Literal
from app import constants as c
from app.models.types import EncryptedStr


class SlackDestination(BaseModel):
    class Config:
        title = c.SLACK
    destination_type: Literal[c.SLACK]
    webhook: EncryptedStr = Field(placeholder="https://hooks.slack.com/services/.../.../...")


class SlackDestination(BaseModel):
    class Config:
        title = c.SLACK
    destination_type: Literal[c.SLACK]
    webhook: EncryptedStr = Field(placeholder="https://hooks.slack.com/services/.../.../...")


class SlackDetails(BaseModel):
    destination_type: Literal[c.SLACK]
    notify_on: Literal["all", "failure", "success"]


class Slack(SlackDestination, SlackDetails):
    pass
