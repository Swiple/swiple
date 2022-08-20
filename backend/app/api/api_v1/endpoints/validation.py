from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from app.db.client import client
from app.settings import settings
from fastapi.param_functions import Depends
from app.core.users import current_active_user

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("")
def list_validations(
        datasource_id: str,
        dataset_id: str,
):
    validations_response = client.search(
        index=settings.VALIDATION_INDEX,
        body=validations_query_body(dataset_id, datasource_id)
    )
    validations_list = [validation["_source"] for validation in validations_response["hits"]["hits"]]

    return JSONResponse(status_code=status.HTTP_200_OK, content=validations_list)


@router.get("/statistics")
def validations(dataset_id: str):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"match": {"dataset_id.keyword": dataset_id}},
                    {"range": {"run_date": {"gte": "now-31d", "lte": "now"}}},
                    {"match": {"exception_info.raised_exception": "false"}},
                ]
            }
        },
        "aggs": {
            "31_day": {
                "filter": {
                    "range": {"run_date": {"gte": "now-31d", "lte": "now"}}
                },
                "aggs": {
                    "success_counts": {
                        "terms": {"field": "success"}
                    }
                }
            },
            "7_day": {
                "filter": {"range": {"run_date": {"gte": "now-7d", "lte": "now"}}},
                "aggs": {
                    "success_counts": {
                        "terms": {"field": "success"}
                    }
                }
            },
            "1_day": {
                "filter": {
                    "range": {"run_date": {"gte": "now-1d", "lte": "now"}},
                },
                "aggs": {
                    "success_counts": {
                        "terms": {"field": "success"},
                    }
                }
            },
            "validation_counts": {
                "date_histogram": {
                    "field": "run_date",
                    "calendar_interval": "1d",
                    "format": "yyyy-MM-dd'T'HH:mm:ssZZZZZ",  # yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ
                },
                "aggs": {
                    "1_day": {
                        "terms": {
                            "field": "success",
                        }
                    }
                }
            }
        }
    }

    validation_stats = client.search(
        index=settings.VALIDATION_INDEX,
        body=query,
    )

    aggs = validation_stats["aggregations"]

    validations_dataset = []
    for daily_bucket in aggs["validation_counts"]["buckets"]:
        objective_pass_rate = calculate_objective_pass_rate(
            buckets=daily_bucket["1_day"]["buckets"],
            doc_count=daily_bucket["doc_count"],
        )
        validations_dataset.append([daily_bucket["key_as_string"], objective_pass_rate])

    one_day_metric = calculate_objective_pass_rate(
        buckets=aggs["1_day"]["success_counts"]["buckets"],
        doc_count=aggs["1_day"]["doc_count"]
    )

    seven_day_metric = calculate_objective_pass_rate(
        buckets=aggs["7_day"]["success_counts"]["buckets"],
        doc_count=aggs["7_day"]["doc_count"]
    )

    thirty_one_day_metric = calculate_objective_pass_rate(
        buckets=aggs["31_day"]["success_counts"]["buckets"],
        doc_count=aggs["31_day"]["doc_count"]
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "1_day_avg": one_day_metric,
            "7_day_avg": seven_day_metric,
            "31_day_avg": thirty_one_day_metric,
            "validations": validations_dataset,
        }
    )


def validations_query_body(datasource_id: str = None, dataset_id: str = None, period: int = 14):
    query = {
        "size": 2000,
        "query": {
            "bool": {
                "must": [
                    {"range": {"run_date": {"gte": f"now-{period}d", "lte": "now"}}},
                ]
            }
        },
        "sort": [{"run_date": "asc"}]
    }
    if not dataset_id and not datasource_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Expected either datasource_id or dataset_id"
        )

    if dataset_id:
        query["query"]["bool"]["must"].append({"match": {"dataset_id.keyword": dataset_id}})

    if datasource_id:
        query["query"]["bool"]["must"].append({"match": {"datasource_id.keyword": datasource_id}})

    return query


def calculate_objective_pass_rate(buckets: list, doc_count: int):
    for bucket in buckets:
        if bucket["key_as_string"] == "true":
            return bucket["doc_count"] / doc_count * 100
