from typing import Optional, get_args
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.shortcuts import delete_by_key_or_404, get_by_key_or_404
from app.models.expectation import ExpectationInput, Expectation
from app.core.expectations import supported_unsupported_expectations
from app import utils
from app.models.validation import Validation
from app.repositories.dataset import DatasetRepository, get_dataset_repository
from app.repositories.datasource import DatasourceRepository, get_datasource_repository
from app.repositories.expectation import ExpectationRepository, get_expectation_repository
from app.repositories.validation import ValidationRepository, get_validation_repository
from app.utils import json_schema_to_single_doc
from fastapi.param_functions import Depends
from app.core.users import current_active_user
import app.constants as c


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
    _table_level_expectation_already_exists(expectation, repository)
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
        validation_repository: ValidationRepository = Depends(get_validation_repository),
):
    expectations = repository.query_by_filter(
        datasource_id=datasource_id,
        dataset_id=dataset_id,
        suggested=suggested,
        enabled=enabled,
        asc=asc,
    )

    if include_history:
        validations = validation_repository.query_by_filter(
            datasource_id=datasource_id,
            dataset_id=dataset_id,
        )

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

    _table_level_expectation_already_exists(expectation, repository)
    return repository.create(expectation.key, expectation)


@router.put("/{expectation_id}", response_model=Expectation)
def update_expectation(
    expectation_id: str,
    expectation_update: Expectation = Depends(get_expectation_payload),
    repository: ExpectationRepository = Depends(get_expectation_repository),
    validation_repository: ValidationRepository = Depends(get_validation_repository),
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
        validation_repository.delete_by_expectation(expectation_id)
        return new_expectation

    return repository.update(expectation_id, expectation, update_dict)


@router.delete("/{expectation_id}")
def delete_expectation(
    expectation_id: str,
    repository: ExpectationRepository = Depends(get_expectation_repository),
    validation_repository: ValidationRepository = Depends(get_validation_repository),
):
    validation_repository.delete_by_expectation(expectation_id)
    delete_by_key_or_404(expectation_id, repository)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="expectation deleted"
    )


def zip_expectations_and_validations(expectations: list[Expectation], validations: list[Validation]):
    expectations_as_dict: dict[str, Expectation] = {}

    for expectation in expectations:
        expectations_as_dict[expectation.key] = expectation

    for validation in validations:
        run_time = utils.string_to_utc_time(validation.meta.run_id.run_time)

        for result in validation.results:
            result_as_dict = result.dict()
            result_as_dict["run_time"] = run_time

            # when an expectation is deleted, the corresponding validation results are not deleted. Instead, validations
            # should be expired/ deleted after some portion of time. For this reason, we only want to zip/join
            # a validation result to an expectation that hasn't been deleted.
            if expectations_as_dict.get(result.expectation_id):
                expectations_as_dict[result.expectation_id].validations.append(result_as_dict)

    return list(expectations_as_dict.values())


def _table_level_expectation_already_exists(expectation: Expectation, repository: ExpectationRepository):
    # Duplicate Table level/ result_type="expectation", expectations are removed by GE when validations are run.
    # Because of this, we want to prevent duplicate table level expectations from being added.
    if expectation.result_type == c.EXPECTATION:
        if repository.count_by_filter(
                dataset_id=expectation.dataset_id,
                enabled=True,
                expectation_type=expectation.expectation_type
        ) > 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Table level expectation_type '{expectation.expectation_type}' already exists"
            )
