from datetime import timedelta, datetime
from typing import List

from opensearchpy.helpers import bulk
from copy import deepcopy

from app.models.dataset import DatasetCreate
from app.models.datasource import DatasourceInput, Engine, PostgreSQL, Athena
from app.settings import settings
from app.db.client import client
from app.models.expectation import ExpectationInput
import uuid
import random
import pytz
import requests
import json
import os

api_url = f"{settings.SWIPLE_API_URL}{settings.API_VERSION}"


expectation_types = [
    "expect_table_columns_to_match_ordered_list",
    "expect_table_row_count_to_be_between",
    "expect_column_values_to_be_in_set",
    "expect_column_values_to_not_be_null",
]


class IntegrationTest:
    def __init__(self):
        self.cookies = None
        self.login()

    def login(self):
        params = {
            "username": os.environ["ADMIN_EMAIL"],
            "password": os.environ["ADMIN_PASSWORD"],
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            f"{api_url}/auth/login",
            data=params,
            headers=headers
        )
        assert response.status_code == 200, json.loads(response.text)["detail"]
        print("Successful login")
        self.cookies = response.cookies.get_dict()

    def add_datasource(self):
        datasource_name = os.environ["DATASOURCE_NAME"]
        self._datasource_exists(datasource_name=datasource_name)

        if os.environ["ENGINE"] == Engine.ATHENA.value:
            datasource: DatasourceInput = DatasourceInput(
                __root__=Athena(
                    engine=Engine.ATHENA,
                    datasource_name=datasource_name,
                    database=os.environ["DATABASE"],
                    region=os.environ["REGION"],
                    s3_staging_dir=os.environ["S3_STAGING_DIR"],
                )
            )
        else:
            datasource: DatasourceInput = DatasourceInput(
                __root__=PostgreSQL(
                    engine=Engine.POSTGRESQL,
                    datasource_name=datasource_name,
                    username=os.environ["USERNAME"],
                    password=os.environ["PASSWORD"],
                    database=os.environ["DATABASE"],
                    host=os.environ["HOST"],
                    port=int(os.environ["PORT"]),
                )
            )
        response = requests.post(
            f"{api_url}/datasources",
            cookies=self.cookies,
            headers={'Content-Type': 'application/json'},
            json=datasource.dict(exclude_none=True),
            params={"test": True}
        )

        assert response.status_code == 200, json.loads(response.text)["detail"]
        print("Successfully added datasource")
        return response.json()

    def add_datasets(
            self,
            datasource_id,
            datasource_name,
    ):
        datasets: List[DatasetCreate] = [
            DatasetCreate(
                datasource_id=datasource_id,
                datasource_name=datasource_name,
                database=os.environ["DATABASE"],
                dataset_name=os.environ["DATASET_NAME"],
            ),
        ]

        dataset_responses = []

        for dataset in datasets:
            response = requests.post(
                f"{api_url}/datasets",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
                json=dataset.dict(exclude_none=True),
            )
            assert response.status_code == 200, json.loads(response.text)["detail"]
            print(f"Successfully added dataset '{dataset.dataset_name}'")

            dataset_responses.append(response.json())

        return dataset_responses

    def suggest(self, datasets):
        suggestion_responses = []

        for dataset in datasets:
            response = requests.post(
                f"{api_url}/datasets/{dataset['key']}/suggest",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
                json=dataset,
            )

            assert response.status_code == 200, json.loads(response.text)["detail"]
            print(f"Successfully added suggestions for dataset '{dataset['dataset_name']}'")

            suggestions = requests.get(
                f"{api_url}/expectations",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
                params={
                    "dataset_id": dataset["key"],
                    "suggested": True,
                    "enabled": False,
                },
            )

            assert suggestions.status_code == 200, json.loads(suggestions.text)["detail"]

            for suggestion in suggestions.json():
                if suggestion["expectation_type"] in expectation_types:
                    suggestion_responses.append(suggestion)

        return suggestion_responses

    def enable_suggestions(self, suggestions):
        for suggestion in suggestions:
            response = requests.put(
                f"{api_url}/expectations/{suggestion['key']}/enable",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
            )

            assert response.status_code == 200, json.loads(response.text)["detail"]

            # set objective
            if suggestion['expectation_type'] in ["expect_column_values_to_not_be_null", "expect_column_values_to_be_in_set"]:
                suggested_expectation = response.json()
                expectation: ExpectationInput = ExpectationInput(
                    **{"__root__": {
                        "dataset_id": suggested_expectation["dataset_id"],
                        "datasource_id": suggested_expectation["datasource_id"],
                        "enabled": suggested_expectation["enabled"],
                        "expectation_type": suggested_expectation["expectation_type"],
                        "kwargs": suggested_expectation["kwargs"],
                    }}
                )

                expectation.__root__.kwargs.objective = 0.95
                response = requests.put(
                    f"{api_url}/expectations/{suggestion['key']}",
                    cookies=self.cookies,
                    headers={'Content-Type': 'application/json'},
                    json=expectation.dict(exclude_none=True),
                )

                assert response.status_code == 200, json.loads(response.text)["detail"]

        print("Successfully enabled suggestions")

    def validate(self, datasets):
        for dataset in datasets:
            response = requests.post(
                f"{api_url}/datasets/{dataset['key']}/validate",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
            )

            assert response.status_code == 200, json.loads(response.text)["detail"]
            print(f"Successfully validated dataset '{dataset['dataset_name']}'")

    def insert_raw_validations(self, validations):
        bulk(
            client,
            validations,
            index=settings.VALIDATION_INDEX,
            refresh="wait_for",
        )

    def generate_historical_validations(self, datasets):
        for dataset in datasets:
            response = requests.get(
                f"{api_url}/expectations",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
                params={
                    "dataset_id": dataset["key"],
                    "enabled": True,
                    "include_history": True,
                },
            )

            assert response.status_code == 200, json.loads(response.text)["detail"]

            expectations = response.json()

            run_ids = [str(uuid.uuid4()) for _ in range(6)]
            number_list = [12.0, 0.0]

            for expectation in expectations:
                validation = expectation["validations"][0]

                validations = []
                # we want to insert 6 days of data so we have 1 week in the UI.
                for i in range(len(run_ids)):
                    validation_copy = deepcopy(validation)
                    validation_copy.update(run_date=str(datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(days=i + 1)))
                    validation_copy.update(run_id=run_ids[i])

                    if expectation["kwargs"].get("objective"):
                        item = random.choices(number_list, cum_weights=(10, 90), k=1)
                        validation_copy["result"]["unexpected_percent"] = item[0]

                        if 100 - item[0] < validation_copy["expectation_config"]["kwargs"]["objective"] * 100:
                            validation_copy.update(success=False)

                    validations.append(validation_copy)

                self.insert_raw_validations(validations)

    def add_resources(self):
        datasource = self.add_datasource()
        print(datasource)

        datasets = self.add_datasets(
            datasource_id=datasource["key"],
            datasource_name=datasource["datasource_name"],
        )
        print(datasets)

        suggestions = self.suggest(datasets=datasets)
        self.enable_suggestions(suggestions=suggestions)
        self.validate(datasets=datasets)

    def _datasource_exists(self, datasource_name):
        response = client.search(
            index=settings.DATASOURCE_INDEX,
            body={"query": {"match": {"datasource_name.keyword": datasource_name}}}
        )

        if response["hits"]["total"]["value"] > 0:
            print(f"Datasource '{datasource_name}' already exists. Deleting it...")
            response = requests.delete(
                f"{api_url}/datasources/{response['hits']['hits'][0]['_id']}",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
            )

            assert response.status_code == 200, json.loads(response.text)["detail"]
            print(f"Successfully deleted datasource '{datasource_name}'")


if __name__ == '__main__':
    IntegrationTest().add_resources()
