import json
from typing import Any

from app.repositories.base import BaseRepository, get_repository
from app.models.dataset import Dataset, Sample
from app.settings import settings


class DatasetRepository(BaseRepository[Dataset]):
    model_class = Dataset
    index = settings.DATASET_INDEX

    def query_by_resource_name(
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
        return self.query(query)

    def _get_dict_from_object(self, object: Dataset) -> dict[str, Any]:
        d = object.dict(by_alias=True)
        sample = object.sample
        if sample is not None:
            sample_dict = {
                **sample.dict(exclude={"rows"}),
                "rows": json.dumps(sample.rows),
            }
            d["sample"] = sample_dict
        return d


get_dataset_repository = get_repository(DatasetRepository)
