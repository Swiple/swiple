from typing import Optional
from pydantic import Field, constr
from app.models.base_model import BaseModel
from app.models.datasource import Engines

class RuntimeParameters(BaseModel):
	schema_name: str = Field(alias="schema")
	query: Optional[str]


class Sample(BaseModel):
	columns: list[str]
	rows: str


class Dataset(BaseModel):
	key: Optional[str]
	datasource_id: str
	datasource_name: str
	engine: Optional[Engines]
	database: str
	connector_type: str = "RuntimeDataConnector"
	dataset_name: str
	description: Optional[constr(max_length=500)]  # requires update in src/screens/datasetOverview/components/DatasetModal
	runtime_parameters: Optional[RuntimeParameters]
	sample: Optional[Sample]
	created_by: Optional[str]
	create_date: Optional[str]
	modified_date: Optional[str]


class ResponseDataset(Dataset):
	key: str
