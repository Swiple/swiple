from typing import Optional
from apscheduler.jobstores.base import JobLookupError
from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.api.shortcuts import get_by_key_or_404
from app.core.users import current_active_user
from app.core.schedulers.scheduler import scheduler, Schedule
from app.repositories.dataset import DatasetRepository, get_dataset_repository
from app.repositories.datasource import DatasourceRepository, get_datasource_repository

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/json-schema")
def json_schema():
    schema = Schedule.schema()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=schema,
    )


@router.get("")
def list_schedules(
    dataset_id: Optional[str] = None,
    datasource_id: Optional[str] = None,
):
    if dataset_id and datasource_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="expected either 'dataset_id' or 'datasource_id'"
        )

    schedules_as_dict = scheduler.list_schedules(
        dataset_id=dataset_id,
        datasource_id=datasource_id,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(schedules_as_dict),
    )


@router.post("")
def create_schedule(
        dataset_id: str,
        schedule: Schedule,
        dataset_repository: DatasetRepository = Depends(get_dataset_repository),
):
    dataset = get_by_key_or_404(dataset_id, dataset_repository)

    schedule = scheduler.add_schedule(
        schedule=schedule,
        datasource_id=dataset.datasource_id,
        dataset_id=dataset_id,
    )
    schedule_as_dict = scheduler.to_dict(schedule)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(schedule_as_dict),
    )


@router.get("/{schedule_id}")
def get_schedule(schedule_id: str):
    schedule = scheduler.get_schedule(schedule_id=schedule_id)

    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Schedule id '{schedule_id}' does not exist"
        )
    schedule_as_dict = scheduler.to_dict(schedule)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(schedule_as_dict)
    )


@router.put("/{schedule_id}")
def update_schedule(
        schedule_id: str,
        schedule: Schedule,
):
    try:
        schedule_as_dict = schedule.trigger.dict(exclude_none=True)
        modified_schedule = scheduler.modify_schedule(
            schedule_id=schedule_id,
            **schedule_as_dict
        )
        schedule_as_dict = scheduler.to_dict(modified_schedule)
    except AttributeError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )
    except JobLookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule id '{schedule_id}' does not exist"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(schedule_as_dict)
    )


@router.delete("/{schedule_id}")
def delete_schedule(
        schedule_id: str
):
    try:
        scheduler.remove_schedule(
            schedule_id=schedule_id
        )
    except JobLookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule id '{schedule_id}' does not exist"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Success"
    )


@router.delete("")
def delete_schedules(
        dataset_id: Optional[str] = None,
        datasource_id: Optional[str] = None,
        dataset_repository: DatasetRepository = Depends(get_dataset_repository),
        datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
):
    if dataset_id and datasource_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="expected either 'dataset_id' or 'datasource_id'"
        )

    if not dataset_id and not datasource_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="expected either 'dataset_id' or 'datasource_id'"
        )

    if dataset_id:
        get_by_key_or_404(dataset_id, dataset_repository)
        scheduler.delete_by_dataset(
            dataset_id=dataset_id,
        )
    elif datasource_id:
        get_by_key_or_404(datasource_id, datasource_repository)
        scheduler.delete_by_datasource(
            datasource_id=datasource_id,
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Success"
    )


@router.post("/next-run-times")
def next_schedule_run_times(
        schedule: Schedule,
):
    next_run_times = scheduler.next_schedule_run_times(
        schedule=schedule
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(next_run_times),
    )
