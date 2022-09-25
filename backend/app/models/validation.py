from typing import Optional, Any, List

from pydantic.config import Extra
from pydantic.fields import Field

from app.models.base_model import BaseModel


class Stats(BaseModel):
    one_day_avg: Optional[float] = Field(alias="1_day_avg")
    seven_day_avg: Optional[float] = Field(alias="7_day_avg")
    thirty_one_day_avg: Optional[float] = Field(alias="31_day_avg")
    validations: Optional[list[Any]]


class Statistics(BaseModel):
    evaluated_expectations: int
    successful_expectations: int
    unsuccessful_expectations: int
    success_percent: float


class ActiveBatchDefinition(BaseModel):
    datasource_name: str
    data_connector_name: str
    data_asset_name: str
    batch_identifiers: dict


class RunId(BaseModel):
    class Config:
        extra = Extra.allow
    run_time: str
    run_name: str


class BatchSpec(BaseModel):
    class Config:
        extra = Extra.allow

    data_asset_name: str
    create_temp_table: bool
    table_name: Optional[str]
    batch_identifiers: Optional[dict]
    schema_name: Optional[str]
    type: Optional[str]
    query: Optional[str]
    temp_table_schema_name: Optional[bool]


class Meta(BaseModel):
    great_expectations_version: str
    expectation_suite_name: str
    run_id: RunId
    batch_spec: dict
    batch_markers: dict
    active_batch_definition: ActiveBatchDefinition
    validation_time: str
    checkpoint_name: Optional[str]
    datasource_id: str
    dataset_id: str


class ExceptionInfo(BaseModel):
    raised_exception: bool
    exception_traceback: Optional[str]
    exception_message: Optional[str]


class Kwargs(BaseModel):
    class Config:
        extra = Extra.allow

    result_format: str
    include_config: bool
    catch_exceptions: bool


class ExpectationConfig(BaseModel):
    kwargs: Kwargs
    expectation_type: str
    meta: dict


class Result(BaseModel):
    exception_info: ExceptionInfo
    success: bool
    expectation_config: ExpectationConfig
    result: dict[str, Any]
    meta: dict[str, Any]
    expectation_id: str


class Validation(BaseModel):
    meta: Meta
    statistics: Statistics
    results: List[Result]
    success: bool
    evaluation_parameters: dict


