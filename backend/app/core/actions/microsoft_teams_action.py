from app.core.actions.base import BaseAction
from app.models.destinations.destination import MicrosoftTeams
from app.settings import settings
import apprise
from apprise import Apprise
import pathlib


class MicrosoftTeamsAction(BaseAction):
    def notify(self, destination: MicrosoftTeams, action_type: str, **kwargs: dict) -> tuple[Apprise, str, str]:
        """
        Send a notification to Microsoft Teams
        :param destination: MicrosoftTeams
        :param action_type: Action type e.g. validation
        :param kwargs: details of the event. E.g. validation
        :return: True if the notification was sent successfully
        """
        if action_type == "validation":
            title, body = self.get_validation(kwargs["validation"])
        else:
            raise NotImplementedError(f"action_type '{action_type}' is not implemented.")

        teams_template_dir = str(pathlib.Path(__file__).parent.resolve())
        template_path = f"{teams_template_dir}/microsoft_teams_template.json"

        ar = apprise.Apprise()
        ar.add(f"{destination.webhook.get_decrypted_value()}?template={template_path}")

        return ar, title, body

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

        run_name = validation["meta"]["run_id"]["run_name"]
        run_time = validation["meta"]["run_id"]["run_time"]

        body = f"""
**Validation Status:** {validation_status}<br/><br/>

**Datasource Name:** {datasource_name}<br/>
**Dataset Name:** {dataset_name}<br/>
**Suite Name:** {suite}<br/><br/>

**Run Name:** {run_name}<br/>
**Run Time:** {run_time}<br/><br/>

**Summary:** {successful_expectations} of {evaluated_expectations} expectations were met.<br/><br/>

**View Results:** {settings.UI_URL}/dataset/home?dataset-id={dataset_id}
        """
        title = f"{validation_status} - {datasource_name}.{dataset_name} [{suite}]"

        return title, body
