from typing import Optional

import pydantic
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.db.client import client
from app.config.settings import settings
from opensearchpy import NotFoundError, RequestError
from app.models import expectation as exp
import json
from fastapi.param_functions import Depends
from app.core.users import current_active_user
from app.api.api_v1.endpoints.expectation import create_expectation
from app.models.expectation import Expectation

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("")
def get_suggestions(
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        asc: Optional[bool] = True,
):
    # TODO implement scrolling
    direction = "asc" if asc else "desc"
    sort_by_key: str = "expectation_type"

    query = {"query": {"match": {}}, "sort": [{sort_by_key: direction}]}

    if datasource_id is None and dataset_id is None:
        query = {"size": 50, "query": {"match_all": {}}, "sort": [{sort_by_key: direction}]}
    else:
        if datasource_id is not None:
            query["query"]["match"]["datasource_id"] = datasource_id

        if dataset_id is not None:
            query["query"]["match"]["dataset_id"] = dataset_id

    try:
        results = client.search(
            index=settings.SUGGESTION_INDEX,
            size=1000,
            body=query
        )["hits"]["hits"]
    except RequestError as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"invalid sort_by_key"
        )

    result_response = []
    for result in results:
        source = result["_source"]
        expectation_type = source["expectation_type"]
        source["kwargs"] = json.loads(source["kwargs"])

        try:
            expectation = exp.type_map[expectation_type](**source)
        except KeyError:
            print(f'expectation_type {expectation_type} not implemented.')
            continue
        except pydantic.ValidationError as ex:
            print(ex)
            continue

        source["documentation"] = expectation.documentation()
        result_response.append(
            dict(**{"key": result["_id"]}, **source)
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=result_response)


@router.get("/{key}")
def get_suggestion(key: str):
    doc = client.get(
        index=settings.SUGGESTION_INDEX,
        id=key
    )["_source"]

    doc["key"] = key

    return JSONResponse(status_code=status.HTTP_200_OK, content=doc)


@router.delete("/{key}")
def delete_suggestion(key: str):
    try:
        client.delete(
            index=settings.SUGGESTION_INDEX, 
            id=key, 
            refresh="wait_for",
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"suggestion with key '{key}' does not exist"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="suggestion deleted"
    )


@router.post("/{key}")
def enable_suggestion(key: str):
    try:
        doc = client.get(
            index=settings.SUGGESTION_INDEX,
            id=key
        )["_source"]
        doc["kwargs"] = json.loads(doc["kwargs"])

        expectation = Expectation.parse_obj(doc)
        create_expectation(expectation)

        client.delete(
            index=settings.SUGGESTION_INDEX,
            id=key,
            refresh="wait_for",
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"suggestion with key '{key}' does not exist"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="suggestion deleted"
    )


def _resource_exists(key: str, index: str, resource_type: str):
    try:
        return client.get(
            index=index,
            id=key
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_type} with id '{key}' does not exist"
        )
