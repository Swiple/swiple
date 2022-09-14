import json
from typing import Any

from app.repositories.base import BaseRepository, get_repository
from app.models.dataset import Dataset, Sample
from app.settings import settings


class DatasetRepository(BaseRepository[Dataset]):
    model_class = Dataset
    index = settings.DATASET_INDEX

    def list_by_resource_name(
        self,
        *,
        datasource_name: str,
        schema: str,
        name: str,
        virtual_name: str,
    ) -> list[Dataset]:
        query = {"query": {"bool": {
            "should": [
                {
                    "bool": {
                        "must": [
                            {"match": {"datasource_name.keyword": datasource_name}},
                            {"match": {"runtime_parameters.schema": schema}},
                            {"match": {"dataset_name.keyword": name}},
                        ],
                    }
                },
                {
                    "bool": {
                        "must": [
                            {"match": {"datasource_name.keyword": datasource_name}},
                            {"match": {"dataset_name.keyword": virtual_name}},
                        ]
                    }
                },
            ]
        }}}
        return self.list(query)

    def create(self, id: str, object: Dataset, *, refresh: str = "wait_for") -> Dataset:
        sample = object.sample
        if sample is not None:
            sample = {**sample.dict(exclude={"rows"}), "rows": json.dumps(sample.rows)}
            object = object.copy(update={"sample": sample})
        return super().create(id, object, refresh=refresh)

    def update(self, id: str, object: Dataset, update_dict: dict[str, Any], *, refresh: str = "wait_for") -> Dataset:
        sample: Sample = update_dict.get("sample")
        if sample is not None:
            update_dict["sample"] = {**sample.dict(exclude={"rows"}), "rows": json.dumps(sample.rows)}
        return super().update(id, object, update_dict, refresh=refresh)


get_dataset_repository = get_repository(DatasetRepository)
