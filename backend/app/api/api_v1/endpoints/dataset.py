import json
from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app import utils
from app.core.users import current_active_user
from app.models.dataset import Dataset, Sample, ResponseDataset
from app.db.client import client
from app.config.settings import settings
from app.utils import get_sample_query
from app.models.datasource import get_datasource
from app.models.users import UserDB
from app.core.dataset import split_dataset_resource
from app.core import security
from app.models.datasource import engine_types
from app.core.runner import Runner
from app.core.expectations import supported_unsupported_expectations
from app import constants as c
from opensearchpy import NotFoundError, RequestError
from opensearchpy.helpers import bulk
import uuid
import requests


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/json-schema")
def get_json_schema():
    schema = Dataset.schema()
    return JSONResponse(status_code=status.HTTP_200_OK, content=schema)


@router.get("", response_model=List[Dataset])
def list_datasets(
        datasource_id: Optional[str] = None,
        sort_by_key: Optional[str] = "dataset_name",
        asc: Optional[bool] = True
):
    # TODO implement scrolling
    direction = "asc" if asc else "desc"

    if datasource_id is None:
        query = {"query": {"match_all": {}}, "sort": [{sort_by_key: direction}]}
    else:
        query = {"query": {"match": {"datasource_id": datasource_id}}, "sort": [{sort_by_key: direction}]}

    try:
        docs = client.search(
            index=settings.DATASET_INDEX,
            size=1000,
            body=query
        )["hits"]["hits"]
    except RequestError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"invalid sort_by_key"
        )

    docs_response = []
    for doc in docs:
        doc["_source"]["key"] = doc["_id"]
        docs_response.append(
            doc["_source"]
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=docs_response)


@router.get("/{key}", response_model=Dataset)
def get_dataset(key: str):
    try:
        doc = _get_dataset(key, as_dict=True)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"dataset with id '{key}' does not exist"
        )

    if doc.get("sample"):
        doc["sample"]["rows"] = json.loads(doc["sample"]["rows"])

    doc["key"] = key
    return JSONResponse(status_code=status.HTTP_200_OK, content=doc)


@router.post("", response_model=Dataset)
def create_dataset(
        dataset: Dataset,
        test_query: bool = True,
        user: UserDB = Depends(current_active_user),
):
    datasource = _check_datasource_exists(dataset.datasource_id)
    _check_dataset_does_not_exists(dataset)

    if test_query:
        response = sample(dataset, False)

        if response.get("exception"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=response.get("exception")
            )

        dataset.sample = Sample(
            columns=response['columns'],
            rows=json.dumps(jsonable_encoder(response['rows'])),
        )

    dataset.engine = datasource.engine
    dataset.created_by = user.email
    dataset.create_date = utils.current_time()
    dataset.modified_date = utils.current_time()

    insert_dataset = client.index(
        index=settings.DATASET_INDEX,
        id=str(uuid.uuid4()),
        body=dataset.dict(by_alias=True),
        refresh="wait_for",
    )

    dataset_as_dict = dataset.dict(by_alias=True)
    dataset_as_dict["key"] = insert_dataset["_id"]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dataset_as_dict
    )


@router.put("/{key}", response_model=ResponseDataset)
def update_dataset(
        dataset: Dataset,
        key: str
):
    original_dataset: Dataset = Dataset(**client.get(
        index=settings.DATASET_INDEX,
        id=key
    )["_source"])

    if original_dataset == dataset:
        return ResponseDataset(key=key, **dataset.dict(by_alias=True))

    if original_dataset.datasource_id != dataset.datasource_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="updates to dataset datasource_id are not supported",
        )

    datasource = _check_datasource_exists(dataset.datasource_id)

    if original_dataset.dataset_name != dataset.dataset_name:
        _check_dataset_does_not_exists(dataset)
        # means it is a physical table.
        if not dataset.runtime_parameters:
            response = sample(dataset, False)

            if response.get("exception"):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=response.get("exception")
                )

            dataset.sample = Sample(
                columns=response['columns'],
                rows=json.dumps(jsonable_encoder(response['rows'])),
            )

    if (
            original_dataset.runtime_parameters and
            dataset.runtime_parameters and
            original_dataset.runtime_parameters.query != dataset.runtime_parameters.query
    ):
        response = sample(dataset, False)

        if response.get("exception"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=response.get("exception")
            )

        dataset.sample = Sample(
            columns=response['columns'],
            rows=json.dumps(jsonable_encoder(response['rows'])),
        )
    dataset.engine = datasource.engine
    dataset.modified_date = utils.current_time()
    dataset.create_date = original_dataset.create_date
    dataset.created_by = original_dataset.created_by

    response = client.update(
        index=settings.DATASET_INDEX,
        id=key,
        body={"doc": dataset.dict(by_alias=True)},
        refresh="wait_for",
    )
    return ResponseDataset(key=response["_id"], **dataset.dict(by_alias=True))


@router.delete("/{key}")
def delete_dataset(
        key: str,
        request: Request
):
    try:
        body = {"query": {"match": {"dataset_id": key}}}

        client.delete_by_query(index=settings.VALIDATION_INDEX, body=body)
        client.delete_by_query(index=settings.EXPECTATION_INDEX, body=body)
        requests.delete(
            url=f"{settings.SCHEDULER_API_URL}/api/v1/schedules",
            params={"dataset_id": key},
            headers=request.headers,
            cookies=request.cookies,
        )
        client.delete(index=settings.DATASET_INDEX, id=key, refresh="wait_for")
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"dataset with id '{key}' does not exist"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="dataset deleted"
    )


@router.post("/sample")
def sample(
        dataset: Dataset,
        response_format: bool = True
):
    datasource = get_datasource(
        key=dataset.datasource_id,
        decrypt_pw=True,
    )

    if dataset.runtime_parameters:
        response = get_sample_query(
            query=dataset.runtime_parameters.query,
            url=datasource.connection_string()
        )
    else:
        response = get_sample_query(
            query=f"select * from {dataset.dataset_name}",
            url=datasource.connection_string(),
        )

    if not response_format:
        return response

    if response.get("exception"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=response.get("exception")
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response)
    )


@router.put("/{key}/sample")
def update_sample(
        key: str
):
    dataset = _get_dataset(key=key)

    response = sample(dataset, False)

    if response.get("exception"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=response.get("exception")
        )

    dataset.sample = Sample(
        columns=response['columns'],
        rows=json.dumps(jsonable_encoder(response['rows'])),
    )

    client.update(
        index=settings.DATASET_INDEX,
        id=key,
        body={"doc": dataset.dict(by_alias=True)},
        refresh="wait_for",
    )
    return JSONResponse(status_code=status.HTTP_200_OK)


@router.post("/{dataset_id}/validate")
def validate_dataset(dataset_id):
    try:
        dataset = client.get(
            index=settings.DATASET_INDEX,
            id=dataset_id,
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"dataset with id '{dataset_id}' does not exist"
        )

    datasource = client.get(
        index=settings.DATASOURCE_INDEX,
        id=dataset["_source"]["datasource_id"],
    )
    datasource["_source"]["datasource_id"] = datasource["_id"]

    expectations_response = client.search(
        index=settings.EXPECTATION_INDEX,
        size=1000,
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"dataset_id": dataset["_id"]}},
                        {"match": {"enabled": True}}
                    ]
                }
            }
        }
    )["hits"]["hits"]

    expectations = []

    identifiers = {
        "run_date": utils.current_time(),
        "run_id": uuid.uuid4(),
        "datasource_id": datasource["_id"],
        "dataset_id": dataset["_id"],
    }

    if datasource["_source"].get("password"):
        datasource["_source"]["password"] = security.decrypt_password(datasource["_source"]["password"])

    engine = engine_types[datasource["_source"]["engine"]]
    datasource = engine(**datasource["_source"])

    dataset = Dataset(**dataset["_source"])

    meta = {
        **datasource.expectation_meta(),
        "dataset_name": dataset.dataset_name,
    }

    for doc in expectations_response:
        doc["_source"]["kwargs"] = json.loads(doc["_source"]["kwargs"])
        doc["_source"]["key"] = doc["_id"]
        doc["_source"]["meta"] = {}
        doc["_source"]["meta"]["expectation_id"] = doc["_id"]
        expectations.append(doc["_source"])

    results = Runner(
        datasource=datasource,
        batch=dataset,
        meta=meta,
        expectations=expectations,
        identifiers=identifiers,
    ).validate()

    _insert_results(results)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(results),
    )


@router.post("/{dataset_id}/suggest")
def create_suggestions(dataset_id):
    try:
        dataset = client.get(
            index=settings.DATASET_INDEX,
            id=dataset_id,
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"dataset with id '{dataset_id}' does not exist"
        )

    datasource = client.get(
        index=settings.DATASOURCE_INDEX,
        id=dataset["_source"]["datasource_id"],
    )
    datasource["_source"]["datasource_id"] = datasource["_id"]

    identifiers = {
        "run_date": utils.current_time(),
        "run_id": uuid.uuid4(),
        "datasource_id": datasource["_id"],
        "dataset_id": dataset["_id"],
    }

    if datasource["_source"].get("password"):
        datasource["_source"]["password"] = security.decrypt_password(datasource["_source"]["password"])

    engine = engine_types[datasource["_source"]["engine"]]
    datasource = engine(**datasource["_source"])

    dataset = Dataset(**dataset["_source"])

    meta = {
        **datasource.expectation_meta(),
        "dataset_name": dataset.dataset_name,
    }

    excluded_expectations = supported_unsupported_expectations()["unsupported_expectations"]
    excluded_expectations.append(c.EXPECT_COLUMN_VALUES_TO_BE_BETWEEN)

    results = Runner(
        datasource=datasource,
        batch=dataset,
        meta=meta,
        identifiers=identifiers,
        datasource_id=dataset.datasource_id,
        dataset_id=dataset_id,
        excluded_expectations=excluded_expectations,
    ).profile()

    client.delete_by_query(
        index=settings.EXPECTATION_INDEX,
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"dataset_id": dataset_id}},
                        {"match": {"suggested": True}},
                        {"match": {"enabled": False}},
                    ]
                }
            }
        }
    )

    for result in results:
        result["enabled"] = False
        result["suggested"] = True

    _insert_results(results, settings.EXPECTATION_INDEX)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(results),
    )


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


def _check_datasource_exists(datasource_id: str):
    try:
        return get_datasource(key=datasource_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"datasource with id '{datasource_id}' does not exist"
        )


def _check_dataset_does_not_exists(dataset: Dataset):
    dataset_schema, dataset_name, is_virtual = split_dataset_resource(dataset)

    query = {"query": {"bool": {
        "should": [
            {
                "bool": {
                    "must": [
                        {"match": {"datasource_name.keyword": dataset.datasource_name}},
                        {"match": {"runtime_parameters.schema": dataset_schema}},
                        {"match": {"dataset_name.keyword": dataset_name}},
                    ],
                }
            },
            {
                "bool": {
                    "must": [
                        {"match": {"datasource_name.keyword": dataset.datasource_name}},
                        {"match": {"dataset_name.keyword": dataset.dataset_name}},
                    ]
                }
            },
        ]
    }}}

    response = client.search(
        index=settings.DATASET_INDEX,
        body=query
    )

    if response["hits"]["total"]["value"] > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"dataset '{dataset.datasource_name}.{dataset_schema}.{dataset_name}' already exists"
        )


def _get_dataset(key: str, as_dict=False):
    dataset = client.get(
        index=settings.DATASET_INDEX,
        id=key
    )["_source"]

    if as_dict:
        return dataset

    return Dataset(**dataset)
