import datetime
from typing import Optional

from apscheduler.jobstores.base import JobLookupError
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.core.users import current_active_user
from app.db.client import client
from opensearchpy import NotFoundError

from app.models.runner import DatasetRun
from app.models.scheduler import Job
from app.core.scheduler import scheduler, to_dict, list_jobs
from app.api.api_v1.endpoints.runner import run_dataset
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import uuid

router = APIRouter(
    # dependencies=[Depends(current_active_user)]
)


@router.get("/json_schema")
def json_schema():
    schema = Job.schema()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=schema,
    )


@router.get("")
def list_all_jobs():
    jobs_as_dict = list_jobs()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(jobs_as_dict),
    )


@router.get("/{dataset_id}")
def list_jobs_for_dataset(
        dataset_id: Optional[str]
):
    jobs_as_dict = list_jobs(
        dataset_id=dataset_id,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(jobs_as_dict),
    )


@router.get("/{job_id}")
def get_job(job_id: str):
    job = scheduler.get_job(job_id=job_id)

    if job is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Job id '{job_id}' does not exist"
        )
    job_as_dict = to_dict(job)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(job_as_dict)
    )


@router.post("/next_run_times")
def get_next_job_run_times(
        job: Job,
):
    if job.trigger.trigger == "cron":
        trigger_type = CronTrigger
    elif job.trigger.trigger == "interval":
        trigger_type = IntervalTrigger
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"{job.trigger.trigger} cannot generate next run times"
        )

    next_run_times = []

    trigger_as_dict = job.trigger.dict(exclude_none=True)
    del trigger_as_dict["trigger"]

    now = datetime.datetime.now(datetime.timezone.utc)

    if job.trigger.start_date and job.trigger.start_date > now:
        next_run_time = job.trigger.start_date
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


@router.post("/{dataset_id}")
def add_job(
        dataset_id: str,
        job: Job,
):
    dataset = _resource_exists(dataset_id)
    datasource_id = dataset["_source"]["datasource_id"]
    dataset_run = DatasetRun(
        dataset_id=dataset_id,
        datasource_id=datasource_id
    )

    job = scheduler.add_job(
        id=f"{dataset_id}__{uuid.uuid4()}",
        func=run_dataset,
        kwargs={'dataset_run': dataset_run},
        misfire_grace_time=job.misfire_grace_time,
        max_instances=job.max_instances,
        **job.trigger.dict(exclude_none=True)
    )
    job_as_dict = to_dict(job)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(job_as_dict),
    )


@router.put("/{job_id}")
def update_job(
        job_id: str,
        job: Job,
):
    try:
        job_as_dict = job.trigger.dict(exclude_none=True)
        rescheduled_job = scheduler.reschedule_job(
            job_id=job_id,
            **job_as_dict
        )
        job_as_dict = to_dict(rescheduled_job)
    except AttributeError as ex:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=str(ex),
        )
    except JobLookupError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Job id '{job_id}' does not exist"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(job_as_dict)
    )


@router.delete("/{job_id}")
def delete_job(
        job_id: str
):
    try:
        scheduler.remove_job(
            job_id=job_id
        )
    except JobLookupError:
        JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Job id '{job_id}' does not exist"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Success"
    )


def _resource_exists(key: str):
    try:
        return client.get(
            index=settings.DATASET_INDEX,
            id=key
        )
    except NotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Dataset with id '{key}' does not exist"
        )
