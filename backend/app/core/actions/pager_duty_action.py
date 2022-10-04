from app.core.actions.base import BaseAction
from app.models.destinations.destination import PagerDuty
import apprise
from apprise import Apprise


class PagerDutyAction(BaseAction):
    def notify(self, destination: PagerDuty, action_type: str, **kwargs) -> tuple[Apprise, str, str]:
        """
        Send a notification to PagerDuty
        :param destination: PagerDuty
        :param action_type: Action type e.g. validation
        :param kwargs: details of the event. E.g. validation
        :return: True if the notification was sent successfully
        """
        if action_type == "validation":
            title, body = self.get_validation(kwargs["validation"])

            datasource_name = kwargs["validation"]["meta"]["active_batch_definition"]["datasource_name"]
            dataset_name = kwargs["validation"]["meta"]["active_batch_definition"]["data_asset_name"]
        else:
            raise NotImplementedError(f"action_type '{action_type}' is not implemented.")

        ar = apprise.Apprise()
        ar.add(f"pagerduty://{destination.integration_key.get_decrypted_value()}@{destination.api_key.get_decrypted_value()}"
               f"?region={destination.region}"
               f"&image=no"
               f"&component={destination.component}"
               f"&source={datasource_name}.{dataset_name}")

        return ar, title, body
