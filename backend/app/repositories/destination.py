from typing import Optional, List

from app.repositories.base import BaseRepository, get_repository
from app.models.destinations.destination import Destination
from app.settings import settings


class DestinationRepository(BaseRepository[Destination]):
    model_class = Destination
    index = settings.DESTINATION_INDEX

    def list(self, *, asc: Optional[bool]) -> list[Destination]:
        direction = "asc" if asc else "desc"
        query = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {"destination_name": direction}
            ]
        }
        return super().query(query, size=1000)

    def query_by_name(self, destination_name: str) -> List[Destination]:
        query = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "destination_name.keyword": destination_name
                        }
                    }
                }
            }
        }
        return self.query(query)

    def count_by_filter(self, *, destination_name: str,):
        query = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "destination_name.keyword": destination_name
                        }
                    }
                }
            }
        }
        return super().count(query)


get_destination_repository = get_repository(DestinationRepository)
