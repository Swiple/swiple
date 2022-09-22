import json
from typing import Any, Optional

from pydantic import Field, constr, validator

from app.models.base_model import BaseModel, CreateUpdateDateModel, KeyModel
from app.models.datasource import Engine

class RuntimeParameters(BaseModel):
	schema_name: str = Field(alias="schema")
	query: Optional[str]


class Sample(BaseModel):
	columns: list[str]
	rows: list[dict[str, Any]]

	@validator("rows", pre=True)
	def parse_json_rows(cls, v: Any):
		if isinstance(v, str):
			return json.loads(v)
		return v


class BaseDataset(BaseModel):
	datasource_id: str
	datasource_name: str
	database: str
	connector_type: str = "RuntimeDataConnector"
	dataset_name: str
	description: Optional[constr(max_length=500)]  # requires update in src/screens/datasetOverview/components/DatasetModal
	runtime_parameters: Optional[RuntimeParameters]

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
