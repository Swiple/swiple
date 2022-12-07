import json
from typing import Any, Optional

from pydantic import Field, constr, validator

from app.models.base_model import BaseModel, CreateUpdateDateModel, KeyModel
from app.models.datasource import Engine
from app.models.sampling import Sampling


class RuntimeParameters(BaseModel):
	schema_name: str = Field(alias="schema")
	query: Optional[str]

	@validator("schema_name")
	def valid_schema_name_format(cls, v):
		if " " in v:
			raise ValueError("should not contain spaces")
		return v


class Sample(BaseModel):
	columns: list[str]
	rows: list[dict[str, Any]]

	@validator("rows", pre=True)
	def parse_json_rows(cls, v: Any):
		if isinstance(v, str):
			return json.loads(v)
		return v


class BaseDataset(BaseModel):
	runtime_parameters: Optional[RuntimeParameters]
	datasource_id: str
	datasource_name: str
	database: str
	connector_type: str = "RuntimeDataConnector"
	description: Optional[constr(max_length=500)]  # requires update in src/screens/datasetOverview/components/DatasetModal
	dataset_name: str
	sampling: Optional[Sampling]

	@validator("dataset_name")
	def dataset_name_should_match_format(cls, v, values, **kwargs):
		if ' ' in v:
			raise ValueError("should not contain spaces")

		if not values.get("runtime_parameters"):
			split_dataset = v.split('.')
			if len(split_dataset) != 2:
				raise ValueError("'dataset_name' should match format 'schema.table' when dataset is a physical table")
		return v

	@validator("sampling")
	def validate_sampling(cls, v, values):
		if v is not None and values.get("runtime_parameters") is not None:
			raise ValueError("sampling cannot be applied to query-based datasets. Apply sampling logic in your query.")
		return v

	def get_resource_names(self) -> tuple[str, str, bool]:
		if self.runtime_parameters:
			dataset_schema = self.runtime_parameters.schema_name
			dataset_name = self.dataset_name
			is_virtual = True
		else:
			split_dataset = self.dataset_name.split('.')
			dataset_schema, dataset_name = split_dataset
			is_virtual = False
		return dataset_schema, dataset_name, is_virtual


class DatasetCreate(BaseDataset):
	pass


class DatasetUpdate(BaseDataset):
	pass


class Dataset(BaseDataset, KeyModel, CreateUpdateDateModel):
	engine: Engine
	sample: Optional[Sample]
	created_by: str
