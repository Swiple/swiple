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


class Scheduler:
    def __init__(self):
        self.scheduler = None

    def start(self):
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
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=utc,
        )
        self.scheduler.start()
        print("-- Scheduler Started --")

    def shutdown(self):
        self.scheduler.shutdown()
        print("-- Scheduler Shutdown --")

    def add_schedule(self, func, *args, **kwargs):
        return self.scheduler.add_schedule(func, *args, **kwargs)

    def modify_schedule(self, schedule_id, jobstore=None, **changes):
        return self.scheduler.modify_job(schedule_id, jobstore, **changes)

    def reschedule_schedule(self, schedule_id, jobstore=None, trigger=None, **trigger_args):
        return self.scheduler.reschedule_job(schedule_id, jobstore, trigger, **trigger_args)

    def pause_schedule(self, schedule_id, jobstore=None):
        return self.scheduler.pause_job(schedule_id, jobstore)

    def resume_schedule(self, schedule_id, jobstore=None):
        return self.scheduler.resume_job(schedule_id, jobstore)

    def remove_schedule(self, schedule_id, jobstore=None):
        self.scheduler.remove_job(schedule_id, jobstore)

    def get_schedule(self, schedule_id):
        return self.scheduler.get_job(schedule_id)

    def get_schedules(self, jobstore=None):
        return self.scheduler.get_jobs(jobstore)

    def get_trigger_fields(self, job: Job):
        trigger_fields = {}

        for field in job.trigger.fields:
            trigger_fields[field.name] = str(field)

        return trigger_fields

    def to_dict(self, job: Job):
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

    def list_schedules(self, datasource_id=None, dataset_id=None):
        schedules = self.scheduler.get_jobs("default")
        schedules_as_dict = []

        for schedule in schedules:
            schedule_as_dict = self.to_dict(schedule)
            schedule_as_dict["expression"] = schedule.trigger.__str__()

            if not datasource_id and not dataset_id:
                schedules_as_dict.append(schedule_as_dict)

            schedule_dataset_id = schedule.id.split("__")[0]

            if not datasource_id and dataset_id and schedule_dataset_id == dataset_id:
                schedules_as_dict.append(schedule_as_dict)

            if not dataset_id and datasource_id and schedule.kwargs['dataset_run'].datasource_id == datasource_id:
                schedules_as_dict.append(schedule_as_dict)

        return schedules_as_dict

    def delete_by_dataset(self, dataset_id):
        schedules = self.list_schedules(
            dataset_id=dataset_id,
        )

        for schedule in schedules:
            self.scheduler.remove_job(schedule["id"])

    def delete_by_datasource(self, datasource_id):
        schedules = self.list_schedules(
            datasource_id=datasource_id,
        )

        for schedule in schedules:
            self.scheduler.remove_job(schedule["id"])


scheduler = Scheduler()
