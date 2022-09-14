import json
from typing import Any, Optional

from app.repositories.base import BaseRepository, get_repository
from app.models.expectation import BaseKwargs, Expectation, type_map
from app.settings import settings


class ExpectationRepository(BaseRepository[Expectation]):
    model_class = Expectation
    index = settings.EXPECTATION_INDEX

    def list_by_filter(
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

        query["query"]["bool"]["must"].append({"match": {"enabled": enabled}})

        if suggested is not None:
            query["query"]["bool"]["must"].append({"match": {"suggested": suggested}})

        if datasource_id is not None:
            query["query"]["bool"]["must"].append({"match": {"datasource_id": datasource_id}})

        if dataset_id is not None:
            query["query"]["bool"]["must"].append({"match": {"dataset_id": dataset_id}})

        return super().list(query, size=1000)

    def create(self, id: str, object: Expectation, *, refresh: str = "wait_for") -> Expectation:
        object = object.copy(update={"kwargs": object.kwargs.json()})
        return super().create(id, object, refresh=refresh)

    def update(self, id: str, object: Expectation, update_dict: dict[str, Any], *, refresh: str = "wait_for") -> Expectation:
        kwargs = update_dict.get("kwargs", object.kwargs)
        update_dict["kwargs"] = json.dumps(kwargs)
        return super().update(id, object, update_dict, refresh=refresh)

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> Expectation:
        try:
            d.pop("key", None)
            expectation_class = type_map[d["expectation_type"]]
            return expectation_class(key=id, **d)
        except KeyError:    
            return super()._get_object_from_dict(d, id=id)


get_expectation_repository = get_repository(ExpectationRepository)
