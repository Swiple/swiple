from app.models.destinations.destination import PagerDuty
from app.settings import settings
import apprise
from apprise import Apprise


class PagerDutyAction:
    def notify(self, action: PagerDuty, action_type: str, **kwargs) -> tuple[Apprise, str, str]:
        """
        Send a notification to PagerDuty
        :param action: PagerDuty action
        :param action_type: Action type e.g. validation
        :param kwargs: Such as, GE Validation
        :return: True if the notification was sent successfully
        """
        if action_type == "validation":
            title, body, datasource_name, dataset_name = self.get_validation(kwargs["validation"])
        else:
            raise NotImplementedError(f"action_type '{action_type}' is not implemented.")

        ar = apprise.Apprise()
        ar.add(f"pagerduty://{action.integration_key.get_decrypted_value()}@{action.api_key.get_decrypted_value()}"
               f"?region={action.region}"
               f"&image=no"
               f"&component={action.component}"
               f"&source={datasource_name}.{dataset_name}")

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

        return title, body, datasource_name, dataset_name
