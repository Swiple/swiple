from typing import Literal
from app.core.actions.email_action import EmailAction
from app.core.actions.slack_action import SlackAction
from app.core.actions.microsoft_teams_action import MicrosoftTeamsAction
from app.core.actions.ops_genie_action import OpsGenieAction
from app.core.actions.pager_duty_action import PagerDutyAction
from apprise import Apprise
import apprise

from app import constants as c
from app.db.client import client
from app.repositories.action import ActionRepository

action_map = {
    c.OPS_GENIE: OpsGenieAction,
    c.SLACK: SlackAction,
    c.EMAIL: EmailAction,
    c.PAGER_DUTY: PagerDutyAction,
    c.MICROSOFT_TEAMS: MicrosoftTeamsAction,
}

ALL = "all"
SUCCESS = "success"
FAILURE = "failure"


def dispatch(
    resource_key: str,
    action_type: Literal["validation"],
    action_status: Literal["success", "failure"],
    **kwargs,
):
    actions = ActionRepository(client).list(
        resource_key=resource_key,
        action_type=action_type,
    )

    if len(actions) == 0:
        return None

    for action in actions:
        try:
            should_dispatch = should_dispatch_notification(
                action_status=action_status,
                notify_on=action.destination.kwargs.notify_on,
            )

            if not should_dispatch:
                continue

            dispatch_action = action_map[action.destination.kwargs.destination_type]

            ar: Apprise
            title: str
            body: str

            ar, title, body = dispatch_action().notify(
                action=action.destination.kwargs,
                action_type=action_type,
                **kwargs,
            )

            with apprise.LogCapture(level=apprise.logging.INFO) as output:
                # Send our notification
                ar.notify(
                    title=title,
                    body=body
                )
                # print(output.getvalue())
            output.close()
        except Exception as e:
            print(e)


def should_dispatch_notification(
        action_status: Literal["success", "failure"],
        notify_on: Literal["all", "success", "failure"],
) -> bool:
    if notify_on == ALL:
        return True

    if action_status == notify_on == SUCCESS:
        return True

    if action_status == notify_on == FAILURE:
        return True

    return False
