from typing import Any, Optional

from app.repositories.base import BaseRepository, get_repository
from fastapi import HTTPException, status
from app.models.validation import Validation
from app.settings import settings


class ValidationRepository(BaseRepository[Validation]):
    model_class = Validation
    index = settings.VALIDATION_INDEX

    def query_by_filter(
        self,
        datasource_id: str = None,
        dataset_id: str = None,
        period: int = 14,
    ):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"meta.run_id.run_time": {"gte": f"now-{period}d", "lte": "now"}}},
                    ]
                }
            },
            "sort": [{"meta.run_id.run_time": "asc"}]
        }

        if dataset_id:
            query["query"]["bool"]["must"].append({"match": {"meta.dataset_id.keyword": dataset_id}})

        if datasource_id:
            query["query"]["bool"]["must"].append({"match": {"meta.datasource_id.keyword": datasource_id}})

        return super().query(query, size=2000)

    def delete_by_filter(
        self,
        dataset_id: str = None,
        datasource_id: str = None,
    ):
        query = {"query": {"bool": {"must": []}}}

        if dataset_id is not None:
            query["query"]["bool"]["must"].append({"match": {"meta.dataset_id.keyword": dataset_id}})
        if datasource_id is not None:
            query["query"]["bool"]["must"].append({"match": {"meta.datasource_id.keyword": datasource_id}})

        return super().delete_by_query(query)

    def delete_by_dataset(self, dataset_id: str):
        return self.delete_by_filter(dataset_id=dataset_id)

    def delete_by_datasource(self, datasource_id: str):
        return self.delete_by_filter(datasource_id=datasource_id)

    def statistics(self, dataset_id):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"meta.dataset_id.keyword": dataset_id}},
                        {"range": {"meta.run_id.run_time": {"gte": "now-31d", "lte": "now"}}},
                        # {"match": {"exception_info.raised_exception": "false"}},
                    ]
                }
            },
            "aggs": {
                "31_day": {
                    "filter": {
                        "range": {"meta.run_id.run_time": {"gte": "now-31d", "lte": "now"}}
                    },
                    "aggs": {
                        "success_counts": {
                            "avg": {"field": "statistics.success_percent"}
                        }
                    }
                },
                "7_day": {
                    "filter": {"range": {"meta.run_id.run_time": {"gte": "now-7d", "lte": "now"}}},
                    "aggs": {
                        "success_counts": {
                            "avg": {"field": "statistics.success_percent"}
                        }
                    }
                },
                "1_day": {
                    "filter": {
                        "range": {"meta.run_id.run_time": {"gte": "now-1d", "lte": "now"}},
                    },
                    "aggs": {
                        "success_counts": {
                            "avg": {"field": "statistics.success_percent"},
                        }
                    }
                },
                "validation_counts": {
                    "date_histogram": {
                        "field": "meta.run_id.run_time",
                        "calendar_interval": "1d",
                        "format": "yyyy-MM-dd'T'HH:mm:ssZZZZZ",  # yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ
                    },
                    "aggs": {
                        "1_day": {
                            "avg": {
                                "field": "statistics.success_percent",
                            }
                        }
                    }
                }
            }
        }
        return self.client.search(
            index=settings.VALIDATION_INDEX,
            body=query,
        )

    def _get_object_from_dict(self, d: dict[str, Any], *, id: Optional[str] = None) -> Validation:
        # if id is not None:
        #     d["key"] = id
        return Validation.parse_obj(d)

    def _get_dict_from_object(self, object: Validation) -> dict[str, Any]:
        return object.dict()


get_validation_repository = get_repository(ValidationRepository)
