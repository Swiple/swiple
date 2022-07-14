from great_expectations.core import ExpectationSuite, ExpectationConfiguration
from great_expectations.core.batch import RuntimeBatchRequest, BatchRequest
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.data_context.types.base import InMemoryStoreBackendDefaults
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from pandas import isnull
import json
import datetime
# TODO, add some "runner_max_batches" to datasource to control the
# max number of batches run at any one time.
from app import utils


class Runner:
    def __init__(self, datasource, batch, meta, dataset_id=None, datasource_id=None, expectations=None,
                 identifiers=None, excluded_expectations=[]):
        self.identifiers = identifiers
        self.datasource = datasource
        self.batch = batch
        self.expectations = expectations
        self.meta = meta
        self.datasource_id = datasource_id
        self.dataset_id = dataset_id
        self.excluded_expectations = excluded_expectations

    def profile(self):
        assert self.datasource_id is not None, 'Require "datasource_id" when profiling.'
        assert self.dataset_id is not None, 'Require "dataset_id" when profiling.'

        data_context_config = self.get_data_context_config()
        context = BaseDataContext(project_config=data_context_config)
        suite: ExpectationSuite = context.create_expectation_suite("suite", overwrite_existing=True)

        batch_request = self.get_batch_request(is_profile=True)

        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite=suite,
        )

        profiler = UserConfigurableProfiler(
            validator,
            excluded_expectations=self.excluded_expectations,
            value_set_threshold="few",
        )
        expectations = profiler.build_suite().to_json_dict()['expectations']

        for expectation in expectations:
            expectation["kwargs"] = json.dumps(expectation["kwargs"])
            expectation["datasource_id"] = self.datasource_id
            expectation["dataset_id"] = self.dataset_id
            expectation["create_date"] = utils.current_time()
            expectation["modified_date"] = utils.current_time()

        return expectations

    def sample(self):
        data_context_config = self.get_data_context_config()
        context = BaseDataContext(project_config=data_context_config)

        batch_request = self.get_batch_request()

        suite: ExpectationSuite = context.create_expectation_suite("suite", overwrite_existing=True)

        try:
            validator = context.get_validator(
                batch_request=batch_request, expectation_suite=suite,
            )
            head = validator.head()
        except KeyError as ex:
            if self.batch.runtime_parameters:
                return {"exception": f"Syntax error in query."}
            else:
                print(str(ex))
                return {"exception": f"{self.batch.dataset_name} is not recognized."}

        rows = head.to_dict(orient='records')
        columns = head.columns

        for record in rows:
            for column in columns:
                if isinstance(record[column], datetime.datetime):
                    record[column] = record[column].__str__()

                if isnull(record[column]):
                    record[column] = None
        return {'columns': list(columns), 'rows': rows}

    def validate(self):
        data_context_config = self.get_data_context_config()
        context = BaseDataContext(project_config=data_context_config)

        suite: ExpectationSuite = context.create_expectation_suite("suite", overwrite_existing=True)

        for expectation in self.expectations:
            if self.batch.runtime_parameters:
                expectation_meta = {**self.meta, **self.batch.runtime_parameters.dict(by_alias=True)}
            else:
                expectation_meta = {**self.meta}

            if expectation.get("meta"):
                expectation_meta = expectation.get("meta")

            expectation_configuration = ExpectationConfiguration(
                expectation_type=expectation["expectation_type"],
                kwargs=expectation["kwargs"],
                meta=expectation_meta,
            )

            suite.add_expectation(expectation_configuration=expectation_configuration)

        batch_request = self.get_batch_request()
        validator = context.get_validator(
            batch_request=batch_request, expectation_suite=suite,
        )

        results = validator.validate().to_json_dict()["results"]

        for result in results:
            if isinstance(result["result"].get("observed_value"), list):
                result["result"]["observed_value_list"] = result["result"].pop("observed_value")

            utils.list_to_string_mapper(result)
            self.identifiers["expectation_id"] = result["expectation_config"]["meta"].pop("expectation_id")
            result.update(self.identifiers)

        return results

    def get_data_context_config(self):
        context = DataContextConfig(
            datasources={
                self.datasource.datasource_name: {
                    "execution_engine": {
                        "class_name": "SqlAlchemyExecutionEngine",
                        "connection_string": self.datasource.connection_string(),
                    },
                    "class_name": "Datasource",
                    "module_name": "great_expectations.datasource",
                    "data_connectors": {
                        "default_runtime_data_connector": {
                            "class_name": "RuntimeDataConnector",

                            # Is there a use-case where this is needed?
                            # If we require users to add all details for runs in the app then
                            # using SDK, it pulls values into SDK? This would require batch_identifiers
                            # for datasources like spark/airflow TODO do this when spark/airflow is added
                            #
                            # Alternative is to let users push to ES runs without
                            # values in app. (Don't like the sound of that...)
                            "batch_identifiers": [
                                self.batch.dataset_name
                            ],
                        },
                        "default_inferred_data_connector_name": {
                            "class_name": "InferredAssetSqlDataConnector",
                            "include_schema_name": True,
                        },
                    }
                }
            },
            store_backend_defaults=InMemoryStoreBackendDefaults(),
            anonymous_usage_statistics={
                "enabled": False,
            }
        )
        return context

    def get_batch_request(self, is_profile=True):
        if self.batch.runtime_parameters:
            batch_spec_passthrough = None
            if is_profile:
                # Bug when profiling. Requires physical/temp table to get column types.
                # set back to False when  https://github.com/great-expectations/great_expectations/issues/4832
                # is fixed
                batch_spec_passthrough = {"create_temp_table": True}

            runtime_parameters = self.batch.runtime_parameters.dict(by_alias=True)
            return RuntimeBatchRequest(
                datasource_name=self.datasource.datasource_name,
                data_connector_name="default_runtime_data_connector",
                data_asset_name=self.batch.dataset_name,
                runtime_parameters=runtime_parameters,
                batch_identifiers={self.batch.dataset_name: self.batch.dataset_name},
                batch_spec_passthrough=batch_spec_passthrough,
            )
        else:
            return BatchRequest(
                datasource_name=self.datasource.datasource_name,
                data_connector_name="default_inferred_data_connector_name",
                data_asset_name=self.batch.dataset_name,
                batch_spec_passthrough={"create_temp_table": False},
            )
