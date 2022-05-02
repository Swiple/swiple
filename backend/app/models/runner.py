from app.models.base_model import BaseModel


class ExpectationRun(BaseModel):
	datasource_id: str
	dataset_id: str
	expectation_id: str


class DatasetRun(BaseModel):
	datasource_id: str
	dataset_id: str


class DatasourceRun(BaseModel):
	datasource_id: str
