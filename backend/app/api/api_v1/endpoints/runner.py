import uuid

from fastapi import APIRouter, HTTPException, status
from opensearchpy.helpers import bulk
from app import utils
from app.core import security
from app.db.client import client
from app.config.settings import settings
from app.models.runner import ExpectationRun, DatasetRun
from app.models.datasource import engine_types
from app.models.dataset import Dataset
from app.core.runner import Runner
from fastapi.param_functions import Depends
from app.core.users import current_active_user
from app.core.expectations import supported_unsupported_expectations
from app import constants as c

import json

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.post("/validate/expectation")
def run_expectation(expectation_run: ExpectationRun):
    docs = client.mget(
        body={
            "docs": [
                {"_index": settings.DATASOURCE_INDEX, "_id": expectation_run.datasource_id},
                {"_index": settings.DATASET_INDEX, "_id": expectation_run.dataset_id},
                {"_index": settings.EXPECTATION_INDEX, "_id": expectation_run.expectation_id},
            ]
        }
    )["docs"]

    datasource = None
    dataset = None
    expectations = []
    meta = {}
    identifiers = {}

    # TODO datasource_id, dataset_id, payloads should match expectations returned by ES
    for doc in docs:
        if doc["_index"] == settings.DATASOURCE_INDEX:
            if doc.get("_source") is None:
                not_found_response("datasource", expectation_run.datasource_id)

            engine = engine_types[doc["_source"]["engine"]]
            datasource = engine(**doc["_source"])

            identifiers["datasource_id"] = doc["_id"]
            identifiers["run_time"] = utils.current_time()

            meta = {**datasource.expectation_meta()}
            continue

        if doc["_index"] == settings.DATASET_INDEX:
            if doc.get("_source") is None:
                not_found_response("dataset", expectation_run.dataset_id)
            dataset = Dataset(**doc["_source"])

            identifiers["dataset_id"] = doc["_id"]
            meta["dataset_name"] = dataset.dataset_name
            continue

        if doc["_index"] == settings.EXPECTATION_INDEX:
            if doc.get("_source") is None:
                not_found_response("expectation", expectation_run.expectation_id)

            doc["_source"]["kwargs"] = json.loads(doc["_source"]["kwargs"])
            doc["_source"]["key"] = doc["_id"]

            expectations.append(doc["_source"])
            identifiers["expectation_id"] = doc["_id"]
            continue
    # raise some exception

    results = Runner(
        datasource=datasource,
        batch=dataset,
        meta=meta,
        expectations=expectations,
        identifiers=identifiers,
    ).validate()

    _insert_results(results)


@router.post("/validate/dataset")
def run_dataset(dataset_run: DatasetRun):
    docs = client.mget(
        body={
            "docs": [
                {"_index": settings.DATASOURCE_INDEX, "_id": dataset_run.datasource_id},
                {"_index": settings.DATASET_INDEX, "_id": dataset_run.dataset_id},
            ]
        }
    )["docs"]

    exp = client.search(
        index=settings.EXPECTATION_INDEX,
        size=1000,
        body={"query": {"match": {"dataset_id": dataset_run.dataset_id}}}
    )

    docs.extend(exp["hits"]["hits"])

    datasource = None
    dataset = None
    expectations = []
    meta = {}
    identifiers = {
        "run_date": utils.current_time(),
        "run_id": uuid.uuid4(),
    }

    # TODO datasource_id, dataset_id, payloads should match expectations returned by ES
    for doc in docs:
        if doc["_index"] == settings.DATASOURCE_INDEX:
            if doc.get("_source") is None:
                not_found_response("datasource", dataset_run.datasource_id)

            if doc["_source"].get("password"):
                doc["_source"]["password"] = security.decrypt_password(doc["_source"]["password"])

            engine = engine_types[doc["_source"]["engine"]]
            datasource = engine(**doc["_source"])

            identifiers["datasource_id"] = doc["_id"]

            meta = {**datasource.expectation_meta()}
            continue

        if doc["_index"] == settings.DATASET_INDEX:
            if doc.get("_source") is None:
                not_found_response("dataset", dataset_run.dataset_id)
            dataset = Dataset(**doc["_source"])

            identifiers["dataset_id"] = doc["_id"]
            meta["dataset_name"] = dataset.dataset_name
            continue

        if doc["_index"] == settings.EXPECTATION_INDEX:
            if doc.get("_source") is None:
                not_found_response("expectations")

            doc["_source"]["kwargs"] = json.loads(doc["_source"]["kwargs"])
            doc["_source"]["key"] = doc["_id"]
            doc["_source"]["meta"] = {}
            doc["_source"]["meta"]["expectation_id"] = doc["_id"]
            expectations.append(doc["_source"])
            continue
    # raise some exception

    results = Runner(
        datasource=datasource,
        batch=dataset,
        meta=meta,
        expectations=expectations,
        identifiers=identifiers,
    ).validate()

    _insert_results(results)


@router.post("/profile/dataset")
def profile_dataset(dataset_run: DatasetRun):
    docs = client.mget(
        body={
            "docs": [
                {"_index": settings.DATASOURCE_INDEX, "_id": dataset_run.datasource_id},
                {"_index": settings.DATASET_INDEX, "_id": dataset_run.dataset_id},
            ]
        }
    )["docs"]

    datasource = None
    dataset = None
    meta = {}
    identifiers = {
        "run_date": utils.current_time(),
        "run_id": uuid.uuid4(),
    }

    for doc in docs:
        if doc["_index"] == settings.DATASOURCE_INDEX:
            if doc.get("_source") is None:
                not_found_response("datasource", dataset_run.datasource_id)

            if doc["_source"].get("password"):
                doc["_source"]["password"] = security.decrypt_password(doc["_source"]["password"])

            engine = engine_types[doc["_source"]["engine"]]
            datasource = engine(**doc["_source"])

            identifiers["datasource_id"] = doc["_id"]

            meta = {**datasource.expectation_meta()}
            continue

        if doc["_index"] == settings.DATASET_INDEX:
            if doc.get("_source") is None:
                not_found_response("dataset", dataset_run.dataset_id)
            dataset = Dataset(**doc["_source"])

            identifiers["dataset_id"] = doc["_id"]
            meta["dataset_name"] = dataset.dataset_name
            continue

    excluded_expectations = supported_unsupported_expectations()["unsupported_expectations"]
    excluded_expectations.append(c.EXPECT_COLUMN_VALUES_TO_BE_BETWEEN)

    results = Runner(
        datasource=datasource,
        batch=dataset,
        meta=meta,
        identifiers=identifiers,
        datasource_id=dataset_run.datasource_id,
        dataset_id=dataset_run.dataset_id,
        excluded_expectations=excluded_expectations,
    ).profile()

    client.delete_by_query(
        index=settings.SUGGESTION_INDEX,
        body={"query": {"match": {"dataset_id": dataset_run.dataset_id}}}
    )

    _insert_results(results, settings.SUGGESTION_INDEX)


def not_found_response(resource_name: str, key=None):
    msg = f"{resource_name} with key '{key}' does not exist"

    if key is None:
        msg = f"no {resource_name} found"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=msg
    )


def _insert_results(results, index: str = settings.VALIDATION_INDEX):
    bulk(
        client,
        results,
        index=index,
        refresh="wait_for",
    )
