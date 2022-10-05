from app.core.actions.base import BaseAction
from app.models.destinations.destination import Email
from app.settings import settings
import apprise
from apprise import Apprise


class EmailAction(BaseAction):
    def notify(self, destination: Email, action_type: str, **kwargs: dict) -> tuple[Apprise, str, str]:
        """
        Send a notification to Email
        :param destination: Email
        :param action_type: Action type e.g. validation
        :param kwargs: details of the event. E.g. validation
        :return: True if the notification was sent successfully
        """
        if action_type == "validation":
            title, body = self.get_validation(kwargs["validation"])
        else:
            raise NotImplementedError(f"action_type '{action_type}' is not implemented.")

        receiver_emails_string = ','.join(destination.receiver_emails)

        ar = apprise.Apprise()
        ar.add(f"mailtos://{destination.smtp_address}:{destination.smtp_port}?"
               f"user={destination.username}&pass={destination.password.get_decrypted_value()}"
               f"&from={destination.sender_alias}&name=Swiple&to={receiver_emails_string}")

        return ar, title, body

    def get_validation(self, validation: dict):
        """
        Creates a message to be dispatched for a validation event.
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

        line_break = "<br/>"
        double_line_break = f"{line_break}{line_break}"

        body = f"""
        Validation Status: {validation_status}{double_line_break}

        Datasource Name: {datasource_name}{line_break}
        Dataset Name: {dataset_name}{line_break}
        Suite Name: {suite}{double_line_break}

        Run Name: {run_id}{line_break}
        Run Time: {run_time}{double_line_break}

        Summary: {successful_expectations} of {evaluated_expectations} expectations were met.{double_line_break}

        View Results: {settings.UI_URL}/dataset/home?dataset-id={dataset_id}
        """
        title = f"{validation_status} - {datasource_name}.{dataset_name} [{suite}]"

        return title, body

