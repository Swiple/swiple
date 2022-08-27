from typing import Optional

from app.core.schedulers.scheduler import Schedule, scheduler
from app.core.users import current_active_user
from app.db.client import client
from app.settings import settings
from apscheduler.jobstores.base import JobLookupError
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from opensearchpy import NotFoundError

router = APIRouter(dependencies=[Depends(current_active_user)])


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
            detail="expected either 'dataset_id' or 'datasource_id'",
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
):
    dataset = _resource_exists(
        settings.DATASET_INDEX,
        dataset_id,
    )

    schedule = scheduler.add_schedule(
        schedule=schedule,
        datasource_id=dataset["_source"]["datasource_id"],
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
            detail=f"Schedule id '{schedule_id}' does not exist",
        )
    schedule_as_dict = scheduler.to_dict(schedule)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(schedule_as_dict)
    )


@router.put("/{schedule_id}")
def update_schedule(
    schedule_id: str,
    schedule: Schedule,
):
    try:
        schedule_as_dict = schedule.trigger.dict(exclude_none=True)
        modified_schedule = scheduler.modify_schedule(
            schedule_id=schedule_id, **schedule_as_dict
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
            detail=f"Schedule id '{schedule_id}' does not exist",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(schedule_as_dict)
    )


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: str):
    try:
        scheduler.remove_schedule(schedule_id=schedule_id)
    except JobLookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule id '{schedule_id}' does not exist",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content="Success")


@router.delete("")
def delete_schedules(
    dataset_id: Optional[str] = None,
    datasource_id: Optional[str] = None,
):
    if dataset_id and datasource_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="expected either 'dataset_id' or 'datasource_id'",
        )

    if not dataset_id and not datasource_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="expected either 'dataset_id' or 'datasource_id'",
        )

    if dataset_id:
        _resource_exists(
            settings.DATASET_INDEX,
            dataset_id,
        )
        scheduler.delete_by_dataset(
            dataset_id=dataset_id,
        )
    elif datasource_id:
        _resource_exists(
            settings.DATASOURCE_INDEX,
            datasource_id,
        )
        scheduler.delete_by_datasource(
            datasource_id=datasource_id,
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content="Success")


@router.post("/next-run-times")
def next_schedule_run_times(
    schedule: Schedule,
):
    next_run_times = scheduler.next_schedule_run_times(schedule=schedule)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(next_run_times),
    )


def _resource_exists(index, key: str):
    try:
        return client.get(index=index, id=key)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{index} with id '{key}' does not exist",
        )
