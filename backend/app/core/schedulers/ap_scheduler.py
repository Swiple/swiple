from typing import List, Dict

from app.core.schedulers.scheduler_interface import SchedulerInterface
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.job import Job
from pytz import utc
from app.settings import settings
import app.constants as c
from app.worker.tasks.validation import run_validation
from app.models.schedule import Schedule
import uuid
import datetime


class ApScheduler(SchedulerInterface):
    def __init__(self):
        self.ap_scheduler: AsyncIOScheduler = None

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
        self.ap_scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=utc,
        )
        self.ap_scheduler.start()
        print("-- Scheduler Started --")

    def shutdown(self):
        self.ap_scheduler.shutdown()
        print("-- Scheduler Shutdown --")

    def add_schedule(self, schedule: Schedule, datasource_id: str, dataset_id: str):
        return self.ap_scheduler.add_job(
            id=f"{datasource_id}__{dataset_id}__{uuid.uuid4()}",
            func=run_validation.delay,
            kwargs={"dataset_id": dataset_id},
            misfire_grace_time=schedule.misfire_grace_time,
            max_instances=schedule.max_instances,
            **schedule.trigger.dict(exclude_none=True)
        )

    def modify_schedule(self, schedule_id, jobstore=None, trigger=None, **trigger_args):
        return self.ap_scheduler.reschedule_job(schedule_id, jobstore, trigger, **trigger_args)

    def pause_schedule(self, schedule_id, jobstore=None):
        return self.ap_scheduler.pause_job(schedule_id, jobstore)

    def resume_schedule(self, schedule_id, jobstore=None):
        return self.ap_scheduler.resume_job(schedule_id, jobstore)

    def remove_schedule(self, schedule_id, jobstore=None):
        self.ap_scheduler.remove_job(schedule_id, jobstore)

    def get_schedule(self, schedule_id):
        return self.ap_scheduler.get_job(schedule_id)

    def list_schedules(self, datasource_id=None, dataset_id=None):
        schedules = self.ap_scheduler.get_jobs("default")
        schedules_as_dict = []

        for schedule in schedules:
            schedule_as_dict = self.to_dict(schedule)
            schedule_as_dict["expression"] = schedule.trigger.__str__()

            if not datasource_id and not dataset_id:
                schedules_as_dict.append(schedule_as_dict)

            schedule_datasource_id, schedule_dataset_id, __ = schedule.id.split("__")

            if not datasource_id and dataset_id and schedule_dataset_id == dataset_id:
                schedules_as_dict.append(schedule_as_dict)

            if not dataset_id and datasource_id and schedule_datasource_id == datasource_id:
                schedules_as_dict.append(schedule_as_dict)

        return schedules_as_dict

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
                "minutes": minutes,
                "hours": hours,
                "days": days,
            }
        if isinstance(job.trigger, DateTrigger):
            trigger_fields["trigger"] = c.DATE
            trigger_fields["run_date"] = job.trigger.run_date
        if isinstance(job.trigger, CronTrigger):
            trigger_fields["trigger"] = c.CRON
            trigger_fields["start_date"] = job.trigger.start_date
            trigger_fields["end_date"] = job.trigger.end_date
            for field in job.trigger.fields:
                if field.name == "second":
                    continue
                trigger_fields[field.name] = str(field)

        job_state["trigger"] = trigger_fields

        return job_state

    def delete_by_dataset(self, dataset_id):
        schedules = self.list_schedules(
            dataset_id=dataset_id,
        )

        for schedule in schedules:
            self.ap_scheduler.remove_job(schedule["id"])

    def delete_by_datasource(self, datasource_id):
        schedules = self.list_schedules(
            datasource_id=datasource_id,
        )

        for schedule in schedules:
            self.ap_scheduler.remove_job(schedule["id"])

    def next_schedule_run_times(self, schedule: Schedule) -> List[Dict]:
        if schedule.trigger.trigger == "cron":
            trigger_type = CronTrigger
        elif schedule.trigger.trigger == "interval":
            trigger_type = IntervalTrigger
        else:
            raise NotImplementedError(
                f"{schedule.trigger.trigger} cannot generate next run times"
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

        return next_run_times


scheduler = ApScheduler()
