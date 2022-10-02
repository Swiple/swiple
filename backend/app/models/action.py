from typing import Literal, Optional
from pydantic.fields import Field

from app.models.base_model import BaseModel, KeyModel, CreateUpdateDateModel
from app.models.destinations.destination import Destination
from app.models.destinations.destination import DestinationDetails, DestinationAction


class DatasetActionRequest(BaseModel):
    resource_key: str
    resource_type: Literal["dataset"]
    destination_key: str
    create_date: Optional[str]
    created_by: Optional[str]
    modified_date: Optional[str]


class DatasetAction(BaseModel):
    resource_key: str
    resource_type: Literal["dataset"]
    destination: Destination
    create_date: Optional[str]
    created_by: Optional[str]
    modified_date: Optional[str]


class ActionRequest(BaseModel):
    resource_key: str
    resource_type: Literal["dataset"]
    action_type: Literal["validation"]
    destination: DestinationDetails


class BaseAction(BaseModel):
    resource_key: str = Field(description="The ID of the resource the action is associated with. E.g. datasource, dataset.")
    resource_type: Literal["dataset"] = Field(description="The resource the action is associated with. E.g. datasource, dataset.")
    action_type: Literal["validation"] = Field(description="The type of event that triggers it.")
    destination: DestinationAction
    created_by: Optional[str]


class ActionUpdate(BaseAction):
    pass


class Action(BaseAction, KeyModel, CreateUpdateDateModel):
    pass
