from typing import Any, Optional
from app.repositories.base import BaseRepository, get_repository
from app.models.datasource import Datasource, engine_types
from app.settings import settings


class DatasourceRepository(BaseRepository[Datasource]):
    model_class = Datasource
    index = settings.DATASOURCE_INDEX

    def get_by_name(self, name: str) -> list[Datasource]:
        return self.list({"query": {"match": {"datasource_name.keyword": name}}})

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> Datasource:
        d.pop("key", None)
        try:
            engine_class = engine_types[d["engine"]]
            return engine_class(key=id, **d)
        except KeyError:    
            return super()._get_object_from_dict(d, id=id)


get_datasource_repository = get_repository(DatasourceRepository)
