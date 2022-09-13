from typing import Any, Generic, Optional, Type, TypeVar

from opensearchpy import OpenSearch, NotFoundError as OSNotFoundError

from app.db.client import client
from app.models.base_model import BaseModel

M = TypeVar("M", bound=BaseModel)


class NotFoundError(OSNotFoundError):
    pass


class BaseRepository(Generic[M]):
    model_class: Type[M]
    index: str

    def __init__(self, client: OpenSearch):
        self.client = client

    def list(self, body: dict[str, Any], *, size: int = 100) -> list[M]:
        response = self.client.search(index=self.index, size=size, body=body)
        results = response["hits"]["hits"]
        return [
            self._get_object_from_dict(result["_source"], id=result["_id"]) for result in results
        ]

    def get(self, id: str) -> M:
        try:
            document = self.client.get(index=self.index, id=id)
        except OSNotFoundError as e:
            raise NotFoundError() from e
        return self._get_object_from_dict(document["_source"], id=document["_id"])

    def create(self, id: str, object: M, *, refresh: str = "wait_for") -> M:
        response = self.client.index(index=self.index, id=id, body=object.dict(), refresh=refresh)
        return self._get_object_from_dict(object.dict(), id=response["_id"])

    def update(self, id: str, object: M, update_dict: dict[str, Any], *, refresh: str = "wait_for") -> M:
        updated_object = object.copy(update=update_dict)
        try:
            self.client.update(
                index=self.index,
                id=id,
                body={"doc": updated_object.dict()},
                refresh=refresh,
            )
        except OSNotFoundError as e:
            raise NotFoundError() from e
        return updated_object

    def delete(self, id: str):
        try:
            self.client.delete(index=self.index, id=id)
        except OSNotFoundError as e:
            raise NotFoundError() from e

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> M:
        return self.model_class(key=id, **d["_source"])


def get_repository(repository_class: Type[BaseRepository]):
    async def _get_repository() -> BaseRepository:
        return repository_class(client)
    return _get_repository
