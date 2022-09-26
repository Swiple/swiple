from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from app.core.users import current_active_user
from app.db.client import client
from app.repositories.dataset import DatasetRepository, get_dataset_repository
from app.repositories.datasource import DatasourceRepository, get_datasource_repository
from app.repositories.expectation import ExpectationRepository, get_expectation_repository
from app.repositories.validation import ValidationRepository, get_validation_repository
from app.settings import settings

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/resource-counts")
def resource_counts(
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
    dataset_repository: DatasetRepository = Depends(get_dataset_repository),
    expectation_repository: ExpectationRepository = Depends(get_expectation_repository),
    validation_repository: ValidationRepository = Depends(get_validation_repository),
):
    # schema_count = client.search(
    #     index=settings.DATASET_INDEX,
    #     body={"size": 0, "aggs": {"item": {"cardinality": {"field": "runtime_parameters.schema"}}}}
    # )["aggregations"]["item"]["value"]

    datasource_count = datasource_repository.count({"query": {"match_all": {}}})
    dataset_count = dataset_repository.count({"query": {"match_all": {}}})
    expectation_count = expectation_repository.count({"query": {"match": {"enabled": True}}})
    validation_count = validation_repository.count({"query": {"match_all": {}}})

    points = get_histogram_points()
    response = {
        "datasource": {
            "count": datasource_count,
            "points": points["datasource"],
        },
        "dataset": {
            "count": dataset_count,
            "points": points["dataset"],
        },
        "expectation": {
            "count": expectation_count,
            "points": points["expectation"],
        },
        "validation": {
            "count": validation_count,
            "points": points["validation"],
        },
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.get("/top-issues")
def top_issues():
    issues_response = client.search(
        index=settings.VALIDATION_INDEX,
        body={
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "meta.run_id.run_time": {
                                    "gte": "now-2d",
                                    "lte": "now"
                                }
                            }
                        },
                        {
                            "range": {
                                "statistics.unsuccessful_expectations": {"gte": 1}
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "dataset_agg": {
                    "terms": {
                        "field": "meta.dataset_id.keyword"
                    },
                    "aggs": {
                        "passed_agg": {
                            "sum": {
                                "field": "statistics.successful_expectations"
                            }
                        },
                        "failed_agg": {
                            "sum": {
                                "field": "statistics.unsuccessful_expectations"
                            }
                        },
                        "total_agg": {
                            "sum": {
                                "field": "statistics.evaluated_expectations"
                            }
                        },
                        "success_rate": {
                            "avg": {
                                "field": "statistics.success_percent"
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

        pass_count = int(bucket["passed_agg"]["value"])
        fail_count = int(bucket["failed_agg"]["value"])
        total_count = int(bucket["total_agg"]["value"])
        dataset_ids[bucket["key"]] = {
            "rate": f'{bucket["success_rate"]["value"]} %',
            "#_failures": f'{fail_count} of {total_count}',
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
            {
                "size": 0,
                "query": {
                    "match": {"enabled": True}
                },
                "aggregations": {
                    "histogram": {
                        "date_histogram": {
                            "field": "create_date",
                            "min_doc_count": 0,
                            "interval": "1d",
                        }
                    }
                }
            },
            {"index": settings.VALIDATION_INDEX},
            histogram_query("meta.run_id.run_time"),
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
