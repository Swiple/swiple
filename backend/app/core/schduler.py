from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.job import Job
import app.constants as c

jobstores = {
    'default': RedisJobStore()
}
executors = {
    'default': ProcessPoolExecutor(5),
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = AsyncIOScheduler(
    jobstores=jobstores, 
    executors={},
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
        for field in job.trigger.fields:
            trigger_fields[field.name] = str(field)

    job_state["trigger"] = trigger_fields

    return job_state


def function():
    print("wooo")

