from typing import Optional, List

from app.models.action import Action
from app.repositories.base import BaseRepository, get_repository
from app.settings import settings


class ActionRepository(BaseRepository[Action]):
    model_class = Action
    index = settings.ACTION_INDEX

    def list(
        self,
        *,
        resource_key: Optional[str] = None,
        action_type: Optional[str] = None,
        destination_name: Optional[str] = None,
        asc: Optional[bool] = True,
    ) -> List[Action]:
        query = self._build_query_filter(
            resource_key=resource_key,
            action_type=action_type,
            destination_name=destination_name,
            asc=asc,
        )
        return super().query(query, size=1000)

    def count_by_filter(
        self,
        *,
        resource_key: Optional[str] = None,
        action_type: Optional[str] = None,
        destination_name: Optional[str] = None,
    ):
        query = self._build_query_filter(
            resource_key=resource_key,
            action_type=action_type,
            destination_name=destination_name,
            asc=None,
        )
        return super().count(query)

    def update_action_by_query(
        self,
        *,
        key: str,
        script_source: str,
        script_params: dict
    ):
        query = {
            "query": {"match": {"destination.key": key}},
            "script": {
                "source": script_source,
                "lang": "painless",
                "params": script_params
            }
        }
        return super().update_by_query(query)

    @staticmethod
    def _build_query_filter(
        *,
        resource_key: Optional[str] = None,
        action_type: Optional[str] = None,
        destination_name: Optional[str] = None,
        asc: Optional[bool] = True,
    ):
        query = {
            "query": {
                "bool": {
                    "must": [

                    ]
                }
            },
        }

        if asc:
            direction = "asc" if asc else "desc"
            query["sort"] = [{"resource_type": direction}]

        if not (resource_key, action_type):
            query = {
                "query": {
                    "match_all": {}
                }
            }

        if resource_key:
            query["query"]["bool"]["must"].append({"match": {"resource_key": resource_key}})

        if action_type:
            query["query"]["bool"]["must"].append({"match": {"action_type": action_type}})

        if destination_name:
            query["query"]["bool"]["must"].append({"match": {"destination.destination_name": destination_name}})

        return query


get_action_repository = get_repository(ActionRepository)
