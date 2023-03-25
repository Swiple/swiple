from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Request
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.api.shortcuts import delete_by_key_or_404, get_by_key_or_404
from app.core.sample import GetSampleException, get_dataset_sample
from app.core.users import current_active_user
from app.models.dataset import BaseDataset, Dataset, DatasetCreate, DatasetUpdate, Sample
from app.models.task import TaskStatus, TaskIdResponse, TaskResultResponse
from app.repositories.dataset import DatasetRepository, get_dataset_repository
from app.repositories.datasource import DatasourceRepository, get_datasource_repository
from app.repositories.expectation import ExpectationRepository, get_expectation_repository
from app.repositories.task import get_task_repository, TaskRepository
from app.repositories.validation import get_validation_repository, ValidationRepository
from app.settings import settings
from app.models.users import UserDB
from opensearchpy import RequestError
import requests
from app.worker.tasks.validation import run_validation
from app.worker.tasks.suggestions import run_suggestions

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
    asc: Optional[bool] = True,
    repository: DatasetRepository = Depends(get_dataset_repository),
):
    # TODO implement scrolling
    direction = "asc" if asc else "desc"

    if datasource_id is None:
        query = {"query": {"match_all": {}}, "sort": [{sort_by_key: direction}]}
    else:
        query = {"query": {"match": {"datasource_id": datasource_id}}, "sort": [{sort_by_key: direction}]}

    try:
        return repository.query(query, size=1000)
    except RequestError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"invalid sort_by_key"
        )


@router.get("/{key}", response_model=Dataset)
def get_dataset(key: str, repository: DatasetRepository = Depends(get_dataset_repository)):
    return get_by_key_or_404(key, repository)


@router.post("", response_model=Dataset)
def create_dataset(
    dataset_create: DatasetCreate,
    test_query: bool = True,
    user: UserDB = Depends(current_active_user),
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
    repository: DatasetRepository = Depends(get_dataset_repository),
):
    datasource = get_by_key_or_404(dataset_create.datasource_id, datasource_repository)
    _check_dataset_does_not_exists(dataset_create, repository)

    dataset = Dataset(
        **dataset_create.dict(by_alias=True),
        engine=datasource.engine,
        created_by=user.email,
    )

    if test_query:
        try:
            data_sample = get_dataset_sample(dataset, datasource)
        except GetSampleException as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.error,
            ) from e
        dataset.sample = data_sample

    return repository.create(dataset.key, dataset)


@router.put("/{key}", response_model=Dataset)
def update_dataset(
    dataset_update: DatasetUpdate,
    key: str,
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
    repository: DatasetRepository = Depends(get_dataset_repository),
):
    dataset = get_by_key_or_404(key, repository)

    if dataset.datasource_id != dataset_update.datasource_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="updates to dataset datasource_id are not supported",
        )

    datasource = get_by_key_or_404(dataset.datasource_id, datasource_repository)

    update_dict = dataset_update.dict(exclude_unset=False, exclude_none=False, by_alias=True)

    if dataset.dataset_name != dataset_update.dataset_name:
        _check_dataset_does_not_exists(dataset_update, repository)

    if should_update_sample(dataset, dataset_update):
        try:
            data_sample = get_dataset_sample(dataset_update, datasource)
        except GetSampleException as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.error,
            ) from e
        update_dict["sample"] = data_sample

    return repository.update(key, dataset, update_dict)


@router.delete("/{key}")
def delete_dataset(
    key: str,
    request: Request,
    repository: DatasetRepository = Depends(get_dataset_repository),
    expectation_repository: ExpectationRepository = Depends(get_expectation_repository),
    validation_repository: ValidationRepository = Depends(get_validation_repository)
):
    get_by_key_or_404(key, repository)

    validation_repository.delete_by_dataset(dataset_id=key)

    # TODO: use an internal function for this rather than making an HTTP request
    requests.delete(
        url=f"{settings.SCHEDULER_API_URL}/api/v1/schedules",
        params={"dataset_id": key},
        headers=request.headers,
        cookies=request.cookies,
    )

    expectation_repository.delete_by_filter(dataset_id=key)
    delete_by_key_or_404(key, repository)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="dataset deleted"
    )


@router.post("/sample", response_model=Sample)
def sample(
    dataset: DatasetCreate,
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
):
    datasource = get_by_key_or_404(dataset.datasource_id, datasource_repository)
    try:
        return get_dataset_sample(dataset, datasource)
    except GetSampleException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.error,
        ) from e


@router.put("/{key}/sample")
def update_sample(
    key: str,
    repository: DatasetRepository = Depends(get_dataset_repository),
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
):
    dataset = get_by_key_or_404(key, repository)
    datasource = get_by_key_or_404(dataset.datasource_id, datasource_repository)
    try:
        data_sample = get_dataset_sample(dataset, datasource)
    except GetSampleException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.error,
        ) from e

    dataset = repository.update(dataset.key, dataset, {"sample": data_sample})
    return dataset


@router.post("/{key}/validate", response_model=TaskIdResponse)
def validate_dataset(
    key: str,
    repository: DatasetRepository = Depends(get_dataset_repository),
):
    get_by_key_or_404(key, repository)
    task = run_validation.delay(dataset_id=key)
    return JSONResponse({"task_id": task.id})


@router.get("/{key}/tasks", response_model=list[TaskResultResponse])
def get_tasks_by_dataset_id(
    key: str,
    status: Optional[TaskStatus] = None,
    dataset_repository: DatasetRepository = Depends(get_dataset_repository),
    repository: TaskRepository = Depends(get_task_repository),
):
    get_by_key_or_404(key, dataset_repository)
    return repository.query_by_dataset_id(
        key,
        status=status,
    )


@router.post("/{key}/suggest", response_model=TaskIdResponse)
def create_suggestions(
    key: str,
    repository: DatasetRepository = Depends(get_dataset_repository),
):
    get_by_key_or_404(key, repository)
    task = run_suggestions.delay(dataset_id=key)
    return JSONResponse({"task_id": task.id})


def should_update_sample(dataset: Dataset, dataset_update: DatasetUpdate):
    # if the new and the old datasets are physical tables and the dataset_name has not changed, don't update sample
    # if the new and the old datasets use a query and the query has not changed, don't update sample
    return not (
        (dataset.dataset_name == dataset_update.dataset_name and (
            dataset.runtime_parameters == dataset_update.runtime_parameters is None)) or
        (dataset.runtime_parameters and
         dataset_update.runtime_parameters and
         dataset.runtime_parameters.query == dataset_update.runtime_parameters.query)
    )


def _check_dataset_does_not_exists(dataset: BaseDataset, repository: DatasetRepository):
    dataset_schema, dataset_name, _ = dataset.get_resource_names()
    existing_datasources = repository.query_by_resource_name(
        datasource_name=dataset.datasource_name,
        schema=dataset_schema,
        name=dataset_name,
        virtual_name=dataset.dataset_name,
    )
    if len(existing_datasources) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"dataset '{dataset.datasource_name}.{dataset_schema}.{dataset_name}' already exists"
        )
