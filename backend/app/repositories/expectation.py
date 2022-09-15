import json
from typing import Any, Optional

from app.repositories.base import BaseRepository, get_repository
from app.models.expectation import BaseKwargs, Expectation, type_map
from app.settings import settings


class ExpectationRepository(BaseRepository[Expectation]):
    model_class = Expectation
    index = settings.EXPECTATION_INDEX

    def query_by_filter(
        self,
        *,
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        suggested: Optional[bool] = None,
        enabled: Optional[bool] = None,
        asc: Optional[bool] = False,
    ) -> list[Exception]:
        direction = "asc" if asc else "desc"
        sort_by_key: str = "expectation_type"

        query = {"query": {"bool": {"must": []}}, "sort": [{sort_by_key: direction}]}

        if enabled is not None:
            query["query"]["bool"]["must"].append({"match": {"enabled": enabled}})

        if suggested is not None:
            query["query"]["bool"]["must"].append({"match": {"suggested": suggested}})

        if datasource_id is not None:
            query["query"]["bool"]["must"].append({"match": {"datasource_id": datasource_id}})

        if dataset_id is not None:
            query["query"]["bool"]["must"].append({"match": {"dataset_id": dataset_id}})

        return super().query(query, size=1000)

    def delete_by_filter(self,
        *,
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        suggested: Optional[bool] = None,
        enabled: Optional[bool] = None,
    ):
        query = {"query": {"bool": {"must": []}}}

        if enabled is not None:
            query["query"]["bool"]["must"].append({"match": {"enabled": enabled}})

        if suggested is not None:
            query["query"]["bool"]["must"].append({"match": {"suggested": suggested}})

        if datasource_id is not None:
            query["query"]["bool"]["must"].append({"match": {"datasource_id": datasource_id}})

        if dataset_id is not None:
            query["query"]["bool"]["must"].append({"match": {"dataset_id": dataset_id}})

        return super().delete_by_query(query)

    def delete_by_datasource(self, datasource_id: str):
        return self.delete_by_filter(datasource_id=datasource_id)

    def _get_dict_from_object(self, object: Expectation) -> dict[str, Any]:
        d = object.dict(by_alias=True)
        kwargs = object.kwargs
        d["kwargs"] = kwargs.json() if isinstance(kwargs, BaseKwargs) else json.dumps(kwargs)
        return d

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> Expectation:
        try:
            expectation_class = type_map[d["expectation_type"]]
            return expectation_class(**d)
        except KeyError:    
            return super()._get_object_from_dict(d)


get_expectation_repository = get_repository(ExpectationRepository)
