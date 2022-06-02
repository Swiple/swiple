from pytz import utc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


class Scheduler:
    def add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)

    def modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def reschedule_job(
        self, job_id, jobstore=None, trigger=None, **trigger_args
    ):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def get_job(self, job_id):
        return scheduler.get_job(job_id)

    def get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)

    def start(self):
        return scheduler.start()


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
    executors=executors, 
    job_defaults=job_defaults, 
    timezone=utc,
)
