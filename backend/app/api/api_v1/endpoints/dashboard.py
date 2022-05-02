from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from app.core.users import current_active_user
from app.db.client import client
from app.config.settings import settings

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/metrics")
def metrics():
    datasource_count = client.count(
        index=settings.DATASOURCE_INDEX,
        body={"query": {"match_all": {}}}
    )

    schema_count = client.search(
        index=settings.DATASET_INDEX,
        body={"size": 0, "aggs": {"item": {"cardinality": {"field": "runtime_parameters.schema"}}}}
    )["aggregations"]["item"]["value"]

    dataset_count = client.count(
        index=settings.DATASET_INDEX,
        body={"query": {"match_all": {}}}
    )

    expectation_count = client.count(
        index=settings.EXPECTATION_INDEX,
        body={"query": {"match_all": {}}}
    )

    validation_count = client.count(
        index=settings.VALIDATION_INDEX,
        body={"query": {"match_all": {}}}
    )

    points = get_histogram_points()
    response = {
        "datasource": {
            "count": datasource_count["count"],
            "points": points["datasource"],
        },
        "dataset": {
            "count": dataset_count["count"],
            "points": points["dataset"],
        },
        "expectation": {
            "count": expectation_count["count"],
            "points": points["expectation"],
        },
        "validation": {
            "count": validation_count["count"],
            "points": points["validation"],
        },
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.get("/issue")
def issues():
    issues_response = client.search(
        index=settings.VALIDATION_INDEX,
        body={
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "run_date": {
                                    "gte": "now-1d",
                                    "lte": "now"
                                }
                            }
                        },
                        {"match": {"exception_info.raised_exception": "false"}}
                    ]
                }
            },
            "aggs": {
                "dataset_agg": {
                    "terms": {
                        "field": "dataset_id.keyword"
                    },
                    "aggs": {
                        "passed_agg": {
                            "filter": {"term": {"success": "true"}}
                        },
                        "success_rate": {
                            "bucket_script": {
                                "buckets_path": {
                                    "doc_count": "_count",
                                    "passed": "passed_agg._count"
                                },
                                "script": "params.passed / params.doc_count * 100"
                            }
                        },
                        "success_rate_bucket_sort": {
                            "bucket_sort": {
                                "sort": {
                                    "success_rate": {
                                        "order": "asc"
                                    }
                                },
                                "size": 10
                            }
                        }
                    }
                }
            }
        }
    )
    buckets = issues_response["aggregations"]["dataset_agg"]["buckets"]

    dataset_id_terms = []
    dataset_ids = {}
    dataset_issues = []

    for bucket in buckets:
        dataset_id_terms.append(bucket["key"])

        pass_count = bucket["passed_agg"]["doc_count"]
        fail_count = bucket["doc_count"] - bucket["passed_agg"]["doc_count"]
        dataset_ids[bucket["key"]] = {
            "rate": f'{bucket["success_rate"]["value"]} %',
            "#_failures": f'{fail_count} of {bucket["doc_count"]}',
            "pass_count": pass_count,
            "fail_count": fail_count,
            "dataset_id": bucket["key"],
        }

    datasets_response = client.search(
        index=settings.DATASET_INDEX,
        body={
            "_source": [
                "datasource_name",
                "dataset_name",
                "dataset_id",
                "datasource_id"
            ],
            "size": 20,
            "query": {
                "terms": {
                    "_id": dataset_id_terms
                }
            }
        }
    )

    for hit in datasets_response["hits"]["hits"]:
        dataset_issues.append({
            **dataset_ids[hit["_id"]],
            **hit["_source"]
        })

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dataset_issues,
    )


def get_histogram_points():
    points_response = client.msearch(
        body=[
            {"index": settings.DATASOURCE_INDEX},
            histogram_query("create_date"),
            {"index": settings.DATASET_INDEX},
            histogram_query("create_date"),
            {"index": settings.EXPECTATION_INDEX},
            histogram_query("create_date"),
            {"index": settings.VALIDATION_INDEX},
            histogram_query("run_date"),
        ]
    )
    # order of list should be the same as order of indices in "body" above
    indices = ["datasource", "dataset", "expectation", "validation"]
    points = {}

    for i in range(len(indices)):
        temp = []
        for point in points_response["responses"][i]["aggregations"]["histogram"]["buckets"]:
            temp.append([point["key_as_string"], point["doc_count"]])
        points[indices[i]] = temp
    return points


def histogram_query(field: str):
    return {
        "size": 0,
        "aggregations": {
            "histogram": {
                "date_histogram": {
                    "field": field,
                    "min_doc_count": 0,
                    "interval": "1d",
                }
            }
        }
    }
