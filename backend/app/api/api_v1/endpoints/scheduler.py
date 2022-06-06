from apscheduler.jobstores.base import JobLookupError
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.core.users import current_active_user
from app.models.scheduler import Job
from app.core.schduler import scheduler, to_dict, function


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("")
def list_jobs():
    jobs = scheduler.get_jobs("default")
    jobs_as_dict = []

    for job in jobs:
        jobs_as_dict.append(to_dict(job))

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


@router.post("")
def add_job(
        job: Job,
):
    job = scheduler.add_job(
        func=function,
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
