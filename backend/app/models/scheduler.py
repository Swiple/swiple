from apscheduler.triggers.cron import BaseField, MonthField, WeekField, DayOfMonthField, DayOfWeekField
from pydantic import validator, Field, Extra
import app.constants as c
from app.models.base_model import BaseModel
from typing import Literal, Union, Optional
from datetime import datetime
from apscheduler.triggers.interval import IntervalTrigger as APSchedulerIntervalTrigger
from apscheduler.triggers.date import DateTrigger as APSchedulerDateTrigger
from apscheduler.triggers.cron import CronTrigger as APSchedulerCronTrigger


class IntervalTrigger(BaseModel):
    trigger: Literal["interval"]
    start_date: Optional[datetime] = Field(description=c.START_DATE)
    end_date: Optional[datetime] = Field(description=c.END_DATE)
    seconds: Optional[int] = Field(ge=1, description=c.SECONDS)
    minutes: Optional[int] = Field(ge=1, description=c.MINUTES)
    hours: Optional[int] = Field(ge=1, description=c.HOURS)
    weeks: Optional[int] = Field(ge=1, description=c.WEEKS)

    @validator("seconds", "minutes", "hours", "weeks")
    def only_one(cls, v, values, field):
        for key, value in values.items():
            if value is not None and key not in ["start_date", "end_date", "trigger"]:
                raise ValueError(f"unexpected property '{field.name}', '{key}' already present")
        return v

    def instance(self):
        return APSchedulerIntervalTrigger(
            **self.dict(exclude={"trigger"})
        )


class CronTrigger(BaseModel):
    trigger: Literal["cron"]
    start_date: Optional[datetime] = Field(description=c.START_DATE)
    end_date: Optional[datetime] = Field(description=c.END_DATE)
    second: Optional[Union[int, str]] = Field(description=c.SECOND)
    minute: Optional[Union[int, str]] = Field(description=c.MINUTE)
    hour: Optional[Union[int, str]] = Field(description=c.HOUR)
    day: Optional[Union[int, str]] = Field(description=c.DAY)
    week: Optional[Union[int, str]] = Field(description=c.WEEK)
    day_of_week: Optional[Union[int, str]] = Field(description=c.DAY_OF_WEEK)
    month: Optional[Union[int, str]] = Field(description=c.MONTH)
    year: Optional[Union[int, str]] = Field(ge=datetime.now().year, description=c.YEAR)

    @validator("year", "month", "day_of_week", "week", "day", "hour", "minute", "second")
    def valid_expressions(cls, v, field):
        fields_map = {
            'year': BaseField,
            'month': MonthField,
            'week': WeekField,
            'day': DayOfMonthField,
            'day_of_week': DayOfWeekField,
            'hour': BaseField,
            'minute': BaseField,
            'second': BaseField
        }
        field_class = fields_map[field.name]
        field_class(field.name, v, False)

        return v


class DateTrigger(BaseModel):
    trigger: Literal["date"]
    run_date: Union[datetime] = Field(description=c.RUN_DATE)


class Job(BaseModel):
    class Config:
        extra = Extra.forbid

    trigger: Union[
        CronTrigger,
        IntervalTrigger,
        DateTrigger
    ] = Field(discriminator="trigger")
    misfire_grace_time: Optional[int] = Field(description=c.MISFIRE_GRACE_TIME)
    max_instances: Optional[int] = Field(description=c.MAX_INSTANCES)


# TODO change undefined
