from app.core.actions.base import BaseAction
from app.models.destinations.destination import Slack
import apprise
from apprise import Apprise


class SlackAction(BaseAction):
    def notify(self, destination: Slack, action_type: str, **kwargs: dict) -> tuple[Apprise, str, str]:
        """
        Send a notification to Slack
        :param destination: Slack
        :param action_type: Action type e.g. validation
        :param kwargs: details of the event. E.g. validation
        :return: True if the notification was sent successfully
        """
        if action_type == "validation":
            title, body = self.get_validation(kwargs["validation"])
        else:
            raise NotImplementedError(f"action_type '{action_type}' is not implemented.")

        ar = apprise.Apprise()
        ar.add(destination.webhook.get_decrypted_value())

        return ar, title, body
