from typing import Any, Generic, Optional, Type, TypeVar

from opensearchpy import OpenSearch, NotFoundError as OSNotFoundError
from opensearchpy.helpers import bulk

from app import utils
from app.db.client import client
from app.models.base_model import BaseModel, CreateUpdateDateModel

M = TypeVar("M", bound=BaseModel)


class NotFoundError(OSNotFoundError):
    pass


class BaseRepository(Generic[M]):
    model_class: Type[M]
    index: str

    def __init__(self, client: OpenSearch):
        self.client = client

    def query(self, body: dict[str, Any], *, size: int = 100) -> list[M]:
        response = self.client.search(index=self.index, size=size, body=body)
        results = response["hits"]["hits"]
        return [
            self._get_object_from_dict(result["_source"], id=result["_id"]) for result in results
        ]

    def count(self, body: dict[str, Any]) -> int:
        return self.client.count(index=self.index, body=body)["count"]

    def get(self, id: str) -> M:
        try:
            document = self.client.get(index=self.index, id=id)
        except OSNotFoundError as e:
            raise NotFoundError() from e
        return self._get_object_from_dict(document["_source"], id=document["_id"])

    def create(self, id: str, object: M, *, refresh: str = "wait_for") -> M:
        body = self._get_dict_from_object(object, exclude={"key"})
        response = self.client.index(index=self.index, id=id, body=body, refresh=refresh)
        return self._get_object_from_dict(self._get_dict_from_object(object), id=response["_id"])

    def update(self, id: str, object: M, update_dict: dict[str, Any], *, refresh: str = "wait_for") -> M:
        # Make sure we don't override create_date
        update_dict.pop("create_date", None)

        updated_object = object.copy(update=update_dict)

        # Update modified_date automatically
        if isinstance(object, CreateUpdateDateModel):
            updated_object.modified_date = utils.current_time()

        try:
            document = self.client.update(
                index=self.index,
                id=id,
                body={"doc": self._get_dict_from_object(updated_object, exclude={"key"})},
                refresh=refresh,
                _source=True,
            )["get"]
        except OSNotFoundError as e:
            raise NotFoundError() from e
        return self._get_object_from_dict(document["_source"], id=id)

    def update_by_query(self, body: dict[str, Any], *, wait_for_completion: bool = True):
        self.client.update_by_query(index=self.index, body=body, wait_for_completion=wait_for_completion)

    def delete(self, id: str, *, refresh: str = "wait_for"):
        try:
            self.client.delete(index=self.index, id=id, refresh=refresh)
        except OSNotFoundError as e:
            raise NotFoundError() from e

    def bulk_create(self, objects: list[M], *, refresh: str = "wait_for"):
        actions = [
            {
                "_op_type": "index",
                "_index": self.index,
                "_id": object.key,
                "_source": self._get_dict_from_object(object, exclude={"key"}),
            } for object in objects
        ]
        bulk(self.client, actions, refresh=refresh)

    def delete_by_query(self, body: dict[str, Any]):
        self.client.delete_by_query(index=self.index, body=body)

    def _get_dict_from_object(self, object: M, **kwargs) -> dict[str, Any]:
        return object.dict(by_alias=True, **kwargs)

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> M:
        if id is not None:
            d["key"] = id
        return self.model_class.parse_obj(d)


R = TypeVar('R', bound=BaseRepository)


def get_repository(repository_class: Type[R]):
    async def _get_repository() -> R:
        return repository_class(client)
    return _get_repository
