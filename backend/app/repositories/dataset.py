import json
from typing import Any, Optional

from fastapi.encoders import jsonable_encoder

from app.repositories.base import BaseRepository, get_repository
from app.models.dataset import Dataset
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

    def delete_by_datasource(self, datasource_id: str):
        query = {"query": {"match": {"datasource_id": datasource_id}}}
        return super().delete_by_query(query)

    def update_datasource(self, datasource_id: str, *, database: Optional[str] = None, datasource_name: Optional[str] = None):
        """
        instead of performing a join on datasource_id in the GET /dataset endpoint,
        we will store the 'datasource_name' and 'database' properties in the
        dataset document. Updates to 'datasource_name' and 'database' are not common
        actions while getting the list of datasets is. Using nested docs was considered,
        but we chose index simplicity over an increase in index load.
        """
        update_by_query_string = ""

        if database is not None:
            update_by_query_string += f"ctx._source.database = '{database}';"

        if datasource_name is not None:
            update_by_query_string += f"ctx._source.datasource_name = '{datasource_name}';"

        if update_by_query_string != "":
            self.client.update_by_query(
                index=self.index,
                body={
                    "query": {"match": {"datasource_id": datasource_id}},
                    "script": {
                        "source": update_by_query_string,
                        "lang": "painless"
                    }
                },
                wait_for_completion=True,
            )

    def _get_dict_from_object(self, object: Dataset, **kwargs) -> dict[str, Any]:
        d = object.dict(by_alias=True, **kwargs)
        sample = object.sample
        if sample is not None:
            sample_dict = {
                **sample.dict(exclude={"rows"}),
                "rows": json.dumps(jsonable_encoder(sample.rows)),
            }
            d["sample"] = sample_dict
        return d


get_dataset_repository = get_repository(DatasetRepository)
