import uuid
import random
import pytz

from app.config.settings import settings
from opensearchpy import OpenSearch
import requests
import json
from datetime import timedelta, datetime
from app import utils
from opensearchpy.helpers import bulk
from copy import deepcopy

api_url = "http://127.0.0.1:8000/api/v1"

client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': settings.OPENSEARCH_PORT}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    # ca_certs=ca_certs_path
)

expectation_types = [
    "expect_table_columns_to_match_ordered_list",
    "expect_table_row_count_to_be_between",
    "expect_column_values_to_be_in_set",
    "expect_column_values_to_not_be_null",
]


class DemoVideoSetup:
    def __init__(self):
        self.cookies = None
        self.login()

    def login(self):
        params = {
            "username": "admin@email.com",
            "password": "admin",
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
        datasource_name = "postgres"
        self._datasource_exists(datasource_name=datasource_name)

        response = requests.post(
            f"{api_url}/datasources",
            cookies=self.cookies,
            headers={'Content-Type': 'application/json'},
            json={
                "engine": "PostgreSQL",
                "datasource_name": datasource_name,
                "username": "postgres",
                "password": "postgres",
                "database": "postgres",
                "host": "postgres",
                "port": 5432,
                "description": "",
            },
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
        datasets = [
            {"datasource_id": datasource_id, "datasource_name": datasource_name, "engine": "PostgreSQL", "dataset_name": "sample_data.orders", "database": "postgres"},
            # {"datasource_id": datasource_id, "datasource_name": datasource_name, "engine": "PostgreSQL", "dataset_name": "sample_data.customer", "database": "postgres"},
            # {"datasource_id": datasource_id, "datasource_name": datasource_name, "engine": "PostgreSQL", "dataset_name": "sample_data.part", "database": "postgres"},
        ]

        dataset_responses = []

        for dataset in datasets:
            response = requests.post(
                f"{api_url}/datasets",
                cookies=self.cookies,
                headers={'Content-Type': 'application/json'},
                json=dataset,
            )

            assert response.status_code == 200, json.loads(response.text)["detail"]
            print(f"Successfully added dataset '{dataset['dataset_name']}'")

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
                expectation = response.json()
                expectation["kwargs"]["objective"] = 0.95
                response = requests.put(
                    f"{api_url}/expectations/{suggestion['key']}",
                    cookies=self.cookies,
                    headers={'Content-Type': 'application/json'},
                    json=expectation,
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

        # datasets = requests.get(
        #     f"{api_url}/datasets",
        #     cookies=self.cookies,
        #     headers={'Content-Type': 'application/json'},
        # ).json()

        self.generate_historical_validations(datasets=datasets)

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
                json={
                    "engine": "PostgreSQL",
                    "datasource_name": "local",
                    "username": "postgres",
                    "password": "postgres",
                    "database": "postgres",
                    "host": "postgres",
                    "port": 5432,
                    "description": "",
                },
                params={"test": True}
            )

            assert response.status_code == 200, json.loads(response.text)["detail"]
            print(f"Successfully deleted datasource '{datasource_name}'")



DemoVideoSetup().add_resources()
