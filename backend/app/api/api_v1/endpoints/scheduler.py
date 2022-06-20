import datetime
import uuid
from typing import Optional

from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from opensearchpy import NotFoundError
from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.core.users import current_active_user
from app.db.client import client
from app.models.runner import DatasetRun
from app.models.schedule import Schedule
from app.core.scheduler import scheduler
from app.api.api_v1.endpoints.runner import run_dataset

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/json_schema")
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
):
    dataset = _resource_exists(
        settings.DATASET_INDEX,
        dataset_id,
    )
    datasource_id = dataset["_source"]["datasource_id"]
    dataset_run = DatasetRun(
        dataset_id=dataset_id,
        datasource_id=datasource_id
    )

    schedule = scheduler.add_schedule(
        id=f"{dataset_id}__{uuid.uuid4()}",
        func=run_dataset,
        kwargs={'dataset_run': dataset_run},
        misfire_grace_time=schedule.misfire_grace_time,
        max_instances=schedule.max_instances,
        **schedule.trigger.dict(exclude_none=True)
    )
    job_as_dict = scheduler.to_dict(schedule)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(job_as_dict),
    )


@router.get("/{schedule_id}")
def get_schedule(schedule_id: str):
    schedule = scheduler.get_schedule(schedule_id=schedule_id)

    if schedule is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Schedule id '{schedule_id}' does not exist"
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
        rescheduled_job = scheduler.reschedule_schedule(
            schedule_id=schedule_id,
            **schedule_as_dict
        )
        schedule_as_dict = scheduler.to_dict(rescheduled_job)
    except AttributeError as ex:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=str(ex),
        )
    except JobLookupError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Schedule id '{schedule_id}' does not exist"
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
        JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Schedule id '{schedule_id}' does not exist"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Success"
    )


@router.delete("")
def delete_schedules(
        dataset_id: Optional[str],
        datasource_id: Optional[str],
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

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Success"
    )


@router.post("/next_run_times")
def get_next_schedule_run_times(
        schedule: Schedule,
):
    if schedule.trigger.trigger == "cron":
        trigger_type = CronTrigger
    elif schedule.trigger.trigger == "interval":
        trigger_type = IntervalTrigger
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"{schedule.trigger.trigger} cannot generate next run times"
        )

    next_run_times = []

    trigger_as_dict = schedule.trigger.dict(exclude_none=True)
    del trigger_as_dict["trigger"]

    now = datetime.datetime.now(datetime.timezone.utc)

    if schedule.trigger.start_date and schedule.trigger.start_date > now:
        next_run_time = schedule.trigger.start_date
    else:
        next_run_time = now

    for _ in range(9):
        next_run_time = trigger_type(
            **trigger_as_dict
        ).get_next_fire_time(next_run_time, next_run_time)

        if not next_run_time:
            break
        next_run_times.append(next_run_time)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(next_run_times),
    )


def _resource_exists(index, key: str):
    try:
        return client.get(
            index=index,
            id=key
        )
    except NotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"{index} with id '{key}' does not exist"
        )
