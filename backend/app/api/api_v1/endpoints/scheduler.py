from apscheduler.jobstores.base import JobLookupError
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.core.users import current_active_user
from app.models.scheduler import Job

from app.models.users import UserDB
from app.core.schduler import scheduler


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("")
def list_jobs():
    job = scheduler.get_jobs("default")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )


@router.get("/{job_id}")
def get_job(job_id: str):
    try:
        job = scheduler.get_job(job_id)
    except JobLookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} does not exist"
        )
    print(job)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )


@router.post("")
def add_job(
        job: Job,
        user: UserDB = Depends(current_active_user),
):
    job = scheduler.add_job()
    print(job)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )


@router.put("/{job_id}")
def update_job(
        job_id: str,
):
    try:
        job = scheduler.modify_job(
            job_id=job_id
        )
    except JobLookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} does not exist"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} does not exist"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )
