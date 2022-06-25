from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from great_expectations.core import ExpectationSuite, ExpectationConfiguration
from great_expectations.core.batch import RuntimeBatchRequest, BatchRequest
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.data_context.types.base import InMemoryStoreBackendDefaults
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()
import time


@app.get("/")
def root():
    profiler = profile()
    print(profiler)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(profiler))


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}


def profile():
    datasource_name = "my_datasource"
    data_asset_name = "tpch_sf1000.lineitem"

    data_context_config = get_data_context_config(datasource_name)
    context = BaseDataContext(project_config=data_context_config)
    suite: ExpectationSuite = context.create_expectation_suite("suite", overwrite_existing=True)

    batch_request = BatchRequest(
        datasource_name=datasource_name,
        data_connector_name="default_inferred_data_connector_name",
        data_asset_name=data_asset_name,
        batch_spec_passthrough={"create_temp_table": False},
    )

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite,
    )

    profiler = UserConfigurableProfiler(
        validator,
        value_set_threshold="few",
    )
    expectations = profiler.build_suite().to_json_dict()['expectations']
    return expectations


def get_data_context_config(datasource_name):
    context = DataContextConfig(
        datasources={
            datasource_name: {
                "execution_engine": {
                    "class_name": "SqlAlchemyExecutionEngine",
                    "connection_string": '',
                },
                "class_name": "Datasource",
                "module_name": "great_expectations.datasource",
                "data_connectors": {
                    "default_runtime_data_connector": {
                        "class_name": "RuntimeDataConnector",
                        "batch_identifiers": [
                            'some_batch_id'
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
        },
        concurrency={
            "enabled": False,
        }
    )
    return context
