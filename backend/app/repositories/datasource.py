from typing import Any, Optional

from app.repositories.base import BaseRepository, get_repository
from app.models.datasource import DatasourceInput, Datasource
from app.settings import settings


class DatasourceRepository(BaseRepository[Datasource]):
    model_class = Datasource
    index = settings.DATASOURCE_INDEX

    def query_by_name(self, name: str) -> list[Datasource]:
        return self.query({"query": {"match": {"datasource_name.keyword": name}}})

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> Datasource:
        if id is not None:
            d["key"] = id
        object = DatasourceInput.parse_obj(d).__root__
        return object


get_datasource_repository = get_repository(DatasourceRepository)
