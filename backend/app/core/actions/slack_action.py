from app.models.destinations.destination import Slack
from app.settings import settings
import apprise
from apprise import Apprise


class SlackAction:
    def notify(self, action: Slack, action_type: str, **kwargs: dict) -> tuple[Apprise, str, str]:
        """
        Send a notification to Slack
        :param action: Slack action
        :param action_type: Action type e.g. validation
        :param kwargs: Such as, GE Validation
        :return: True if the notification was sent successfully
        """
        if action_type == "validation":
            title, body = self.get_validation(kwargs["validation"])
        else:
            raise NotImplementedError(f"action_type '{action_type}' is not implemented.")

        ar = apprise.Apprise()
        ar.add(action.webhook.get_decrypted_value())

        return ar, title, body

    def get_validation(self, validation: dict):
        evaluated_expectations = validation["statistics"]["evaluated_expectations"]
        successful_expectations = validation["statistics"]["successful_expectations"]

        validation_status = "Success 🎉" if validation["success"] else "Failure ❌"
        suite = validation["meta"]["expectation_suite_name"]
        datasource_name = validation["meta"]["active_batch_definition"]["datasource_name"]
        dataset_name = validation["meta"]["active_batch_definition"]["data_asset_name"]
        dataset_id = validation["meta"]["dataset_id"]

        run_id = validation["meta"]["run_id"]["run_name"]
        run_time = validation["meta"]["run_id"]["run_time"]

        body = f"""
Validation Status: {validation_status}

Datasource Name: {datasource_name}
Dataset Name: {dataset_name}
Suite Name: {suite}

Run Name: {run_id}
Run Time: {run_time}

Summary: {successful_expectations} of {evaluated_expectations} expectations were met.

View Results: {settings.UI_URL}/dataset/home?dataset-id={dataset_id}
        """
        title = f"{validation_status} - {datasource_name}.{dataset_name} [{suite}]"

        return title, body
