from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.job import Job
from pytz import utc

from app.config.settings import settings
import app.constants as c

jobstores = {
    'default': RedisJobStore(
        db=settings.SCHEDULER_REDIS_DB,
        **settings.SCHEDULER_REDIS_KWARGS,
    )
}
executors = {
    'default': ProcessPoolExecutor(
        max_workers=settings.SCHEDULER_EXECUTOR_MAX_WORKERS,
        pool_kwargs=settings.SCHEDULER_EXECUTOR_KWARGS,
    )
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = AsyncIOScheduler(
    jobstores=jobstores, 
    executors=executors,
    job_defaults=job_defaults, 
    timezone=utc,
)
scheduler.start()


def get_trigger_fields(job: Job):
    trigger_fields = {}

    for field in job.trigger.fields:
        trigger_fields[field.name] = str(field)

    return trigger_fields


def to_dict(job: Job):
    job_state = job.__getstate__()
    trigger_fields = {}

    if isinstance(job.trigger, IntervalTrigger):
        ts = job.trigger.interval.total_seconds()

        weeks, r = divmod(ts, 604800)
        days, r = divmod(r, 86400)
        hours, r = divmod(r, 3600)
        minutes, seconds = divmod(r, 60)

        trigger_fields = {
            "trigger": c.INTERVAL,
            "start_date": job.trigger.start_date,
            "end_date": job.trigger.end_date,
            "seconds": seconds,
            "minutes": minutes,
            "hours": hours,
            "days": days,
            "weeks": weeks,
        }
    if isinstance(job.trigger, DateTrigger):
        trigger_fields["trigger"] = c.DATE
        trigger_fields["run_date"] = job.trigger.run_date
    if isinstance(job.trigger, CronTrigger):
        trigger_fields["trigger"] = c.CRON
        trigger_fields["start_date"] = job.trigger.start_date
        trigger_fields["end_date"] = job.trigger.end_date
        for field in job.trigger.fields:
            trigger_fields[field.name] = str(field)

    job_state["trigger"] = trigger_fields

    return job_state


def list_jobs(datasource_id=None, dataset_id=None):
    jobs = scheduler.get_jobs("default")
    jobs_as_dict = []

    for job in jobs:
        job_as_dict = to_dict(job)
        job_as_dict["expression"] = job.trigger.__str__()

        if not datasource_id and not dataset_id:
            jobs_as_dict.append(job_as_dict)

        if not datasource_id and dataset_id and job.id.startswith(dataset_id):
            jobs_as_dict.append(job_as_dict)

        if not dataset_id and datasource_id and job.kwargs['dataset_run'].datasource_id == datasource_id:
            jobs_as_dict.append(job_as_dict)

    return jobs_as_dict


def delete_by_dataset(dataset_id):
    jobs = list_jobs(
        dataset_id=dataset_id,
    )

    for job in jobs:
        scheduler.remove_job(job["id"])


def delete_by_datasource(datasource_id):
    jobs = list_jobs(
        datasource_id=datasource_id,
    )

    for job in jobs:
        scheduler.remove_job(job["id"])
