from pydantic.fields import Field
from typing import Optional, Union

from app import constants as c
from app.models.base_model import BaseModel, KeyModel, CreateUpdateDateModel
from app.models.destinations.slack import (
    Slack,
    SlackDestination,
    SlackDetails,
)
from app.models.destinations.pager_duty import (
    PagerDuty,
    PagerDutyDestination,
    PagerDutyDetails,
)
from app.models.destinations.microsoft_teams import (
    MicrosoftTeams,
    MicrosoftTeamsDestination,
    MicrosoftTeamsDetails,
)
from app.models.destinations.email import (
    Email,
    EmailDestination,
    EmailDetails,
)
from app.models.destinations.ops_genie import (
    OpsGenie,
    OpsGenieDestination,
    OpsGenieDetails,
)

DestinationKwargs = Union[
    OpsGenieDestination,
    SlackDestination,
    EmailDestination,
    MicrosoftTeamsDestination,
    PagerDutyDestination,
]


class BaseDestination(BaseModel):
    destination_name: str
    kwargs: DestinationKwargs = Field(discriminator="destination_type")
    created_by: Optional[str]


class DestinationDetails(BaseModel):
    destination_name: str
    kwargs: Union[
        OpsGenieDetails,
        SlackDetails,
        EmailDetails,
        MicrosoftTeamsDetails,
        PagerDutyDetails,
    ] = Field(discriminator="destination_type")


class DestinationAction(BaseModel):
    key: str
    destination_name: str
    kwargs: Union[
        OpsGenie,
        Slack,
        Email,
        MicrosoftTeams,
        PagerDuty,
    ] = Field(discriminator="destination_type")


class DestinationUpdate(BaseDestination):
    pass


class Destination(BaseDestination, KeyModel, CreateUpdateDateModel):
    pass


destinations_map = {
    c.OPS_GENIE: OpsGenieDestination,
    c.SLACK: SlackDestination,
    c.EMAIL: EmailDestination,
    c.MICROSOFT_TEAMS: MicrosoftTeamsDestination,
    c.PAGER_DUTY: PagerDutyDestination,
}

destination_details_map = {
    c.OPS_GENIE: OpsGenieDetails,
    c.SLACK: SlackDetails,
    c.EMAIL: EmailDetails,
    c.MICROSOFT_TEAMS: MicrosoftTeamsDetails,
    c.PAGER_DUTY: PagerDutyDetails,
}
