from apprise import Apprise
from app.models.destinations.destination import DestinationKwargs
from app.settings import settings


class BaseAction:
    def notify(self, destination: DestinationKwargs, action_type: str, **kwargs: dict) -> tuple[Apprise, str, str]:
        """
        Send a notification to destionation e.g. Email, OpsGenie, etc.
        :param destination: Destination kwargs
        :param action_type: Action type e.g. validation
        :param kwargs: Such as, GE Validation
        :return: True if the notification was sent successfully
        """
        pass

    def get_validation(self, validation: dict):
        """
        Creates a message to be dispatched for a validation event.
        :param validation: Details of the validation
        """
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
