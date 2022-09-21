from typing import Optional, get_args
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.shortcuts import delete_by_key_or_404, get_by_key_or_404
from app.models.expectation import ExpectationInput, Expectation
from app.core.expectations import supported_unsupported_expectations
from app import utils
from app.db.client import client
from app.repositories.dataset import DatasetRepository, get_dataset_repository
from app.repositories.datasource import DatasourceRepository, get_datasource_repository
from app.repositories.expectation import ExpectationRepository, get_expectation_repository
from app.settings import settings
from app.utils import json_schema_to_single_doc
from app.api.api_v1.endpoints import validation
from fastapi.param_functions import Depends
from app.core.users import current_active_user


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)

async def get_expectation_payload(expectation: ExpectationInput) -> Expectation:
    return expectation.__root__


@router.get("/json-schema")
def get_json_schema():
    expectations = []
    for expectation in get_args(Expectation):
        json_schema = json_schema_to_single_doc(expectation.schema())
        expectations.append(json_schema)

    return JSONResponse(status_code=status.HTTP_200_OK, content=expectations)


@router.get("/supported")
def list_supported_expectations():
    content = supported_unsupported_expectations()
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.put("/{expectation_id}/enable", response_model=Expectation)
def enable_expectation(
        expectation_id: str,
        repository: ExpectationRepository = Depends(get_expectation_repository),
):
    expectation = get_by_key_or_404(expectation_id, repository)
    return repository.update(expectation_id, expectation, {"enabled": True})


@router.put("/{expectation_id}/disable", response_model=Expectation)
def disable_expectation(
        expectation_id: str,
        repository: ExpectationRepository = Depends(get_expectation_repository),
):
    expectation = get_by_key_or_404(expectation_id, repository)
    return repository.update(expectation_id, expectation, {"enabled": False})


@router.get("", response_model=list[Expectation])
def list_expectations(
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        include_history: Optional[bool] = False,
        suggested: Optional[bool] = None,
        enabled: Optional[bool] = True,
        asc: Optional[bool] = False,
        repository: ExpectationRepository = Depends(get_expectation_repository),
):
    expectations = repository.query_by_filter(
        datasource_id=datasource_id,
        dataset_id=dataset_id,
        suggested=suggested,
        enabled=enabled,
        asc=asc,
    )

    if include_history:
        results = client.search(
            body=validation.validations_query_body(datasource_id, dataset_id),
            index=settings.VALIDATION_INDEX,
        )
        validations = results["hits"]["hits"]

        return zip_expectations_and_validations(expectations, validations)

    return expectations


@router.get("/{expectation_id}", response_model=Expectation)
def get_expectation(
    expectation_id: str,
    repository: ExpectationRepository = Depends(get_expectation_repository),
):
    return get_by_key_or_404(expectation_id, repository)


@router.post("", response_model=Expectation)
def create_expectation(
    expectation: Expectation = Depends(get_expectation_payload),
    repository: ExpectationRepository = Depends(get_expectation_repository),
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
    dataset_repository: DatasetRepository = Depends(get_dataset_repository),
):
    get_by_key_or_404(expectation.datasource_id, datasource_repository)
    dataset = get_by_key_or_404(expectation.dataset_id, dataset_repository)

    if dataset.datasource_id != expectation.datasource_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="expectation datasource_id does not match dataset datasource_id"
        )

    return repository.create(expectation.key, expectation)


@router.put("/{expectation_id}", response_model=Expectation)
def update_expectation(
    expectation_id: str,
    expectation_update: Expectation = Depends(get_expectation_payload),
    repository: ExpectationRepository = Depends(get_expectation_repository),
):
    expectation = get_by_key_or_404(expectation_id, repository)
    update_dict = expectation_update.dict(exclude={"key"})

    if expectation.datasource_id != expectation_update.datasource_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="updates to expectation datasource_id are not supported",
        )

    if expectation.dataset_id != expectation_update.dataset_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="updates to expectation dataset_id are not supported",
        )

    # This allows the user to edit an existing
    # expectations expectation_type without having to
    # delete it and create a new one. We handle it for them.
    # We want to delete the existing expectation in-case we
    # decide to run aggregations on validations that have been
    # run. We can't have an expectation with the same id but
    # with different expectation types
    if expectation.expectation_type != expectation_update.expectation_type:
        new_expectation = repository.create(expectation_update.key, expectation_update)

        repository.delete(expectation_id)
        client.delete_by_query(
            index=settings.VALIDATION_INDEX,
            body={"query": {"match": {"expectation_id": expectation_id}}}
        )
        return new_expectation

    return repository.update(expectation_id, expectation, update_dict)


@router.delete("/{expectation_id}")
def delete_expectation(
    expectation_id: str,
    repository: ExpectationRepository = Depends(get_expectation_repository),
):
    client.delete_by_query(
        index=settings.VALIDATION_INDEX,
        body={"query": {"match": {"expectation_id": expectation_id}}}
    )
    delete_by_key_or_404(expectation_id, repository)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="expectation deleted"
    )


def zip_expectations_and_validations(expectations: list[Expectation], validations):

    expectations_as_dict: dict[str, Expectation] = {}

    for expectation in expectations:
        expectations_as_dict[expectation.key] = expectation

    for v in validations:
        source = v["_source"]
        source["run_date"] = utils.string_to_military_time(source["run_date"])
        expectations_as_dict[source["expectation_id"]].validations.append(source)

    return list(expectations_as_dict.values())
