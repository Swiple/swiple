import json
from typing import Any, Optional

from app.models.base_model import BaseModel
from app.repositories.base import BaseRepository, get_repository
from app.models.expectation import Expectation, ExpectationInput
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
        expectation_type: Optional[str] = None
    ) -> list[Expectation]:
        direction = "asc" if asc else "desc"
        sort_by_key: str = "expectation_type"
        sort = {"sort": [{sort_by_key: direction}]}

        query = self._build_query_filter(
            datasource_id=datasource_id,
            dataset_id=dataset_id,
            suggested=suggested,
            enabled=enabled,
            expectation_type=expectation_type,
            sort=sort,
        )
        return super().query(query, size=1000)

    def count_by_filter(
        self,
        *,
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        suggested: Optional[bool] = None,
        enabled: Optional[bool] = None,
        expectation_type: Optional[str] = None
    ):
        query = self._build_query_filter(
            datasource_id=datasource_id,
            dataset_id=dataset_id,
            suggested=suggested,
            enabled=enabled,
            expectation_type=expectation_type,
        )
        return super().count(query)

    def delete_by_filter(
        self,
        *,
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        suggested: Optional[bool] = None,
        enabled: Optional[bool] = None,
    ):
        query = self._build_query_filter(
            datasource_id=datasource_id,
            dataset_id=dataset_id,
            suggested=suggested,
            enabled=enabled,
        )

        return super().delete_by_query(query)

    def delete_by_datasource(self, datasource_id: str):
        return self.delete_by_filter(datasource_id=datasource_id)

    def _get_dict_from_object(self, object: Expectation, **kwargs) -> dict[str, Any]:
        d = object.dict(by_alias=True, **kwargs)
        kwargs = object.kwargs
        d["kwargs"] = kwargs.json() if isinstance(kwargs, BaseModel) else json.dumps(kwargs)
        return d

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> Expectation:
        if id is not None:
            d["key"] = id
        object = ExpectationInput.parse_obj(d).__root__
        object.documentation = object._documentation()
        return object

    @staticmethod
    def _build_query_filter(
        *,
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        suggested: Optional[bool] = None,
        enabled: Optional[bool] = None,
        expectation_type: Optional[str] = None,
        sort: Optional[dict] = None,
    ):
        if sort is None:
            sort = {}

        query = {"query": {"bool": {"must": []}}, **sort}

        if enabled is not None:
            query["query"]["bool"]["must"].append({"match": {"enabled": enabled}})

        if suggested is not None:
            query["query"]["bool"]["must"].append({"match": {"suggested": suggested}})

        if datasource_id is not None:
            query["query"]["bool"]["must"].append({"match": {"datasource_id": datasource_id}})

        if dataset_id is not None:
            query["query"]["bool"]["must"].append({"match": {"dataset_id": dataset_id}})

        if expectation_type is not None:
            query["query"]["bool"]["must"].append({"match": {"expectation_type": expectation_type}})

        return query


get_expectation_repository = get_repository(ExpectationRepository)
