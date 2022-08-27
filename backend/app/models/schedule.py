from datetime import datetime
from typing import Literal, Optional, Union

import app.constants as c
from app.models.base_model import BaseModel
from apscheduler.triggers.cron import (
    BaseField,
    DayOfMonthField,
    DayOfWeekField,
    MonthField,
    WeekField,
)
from pydantic import Extra, Field, validator


class IntervalTrigger(BaseModel):
    class Config:
        title = "Interval"

    trigger: Literal["interval"]
    start_date: Optional[datetime] = Field(description=c.START_DATE)
    end_date: Optional[datetime] = Field(description=c.END_DATE)
    seconds: Optional[int] = Field(description=c.SECONDS)
    minutes: Optional[int] = Field(description=c.MINUTES)
    hours: Optional[int] = Field(description=c.HOURS)
    days: Optional[int] = Field(description=c.DAYS)
    weeks: Optional[int] = Field(description=c.WEEKS)

    @validator("end_date")
    def start_date_before_end_date(cls, v, values):
        if v and values["start_date"] and v < values["start_date"]:
            raise ValueError("end_date should not be before start_date")
        return v


class CronTrigger(BaseModel):
    class Config:
        title = "Cron"

    trigger: Literal["cron"]
    start_date: Optional[datetime] = Field(description=c.START_DATE)
    end_date: Optional[datetime] = Field(description=c.END_DATE)
    second: Optional[str] = Field(description=c.SECOND)
    minute: Optional[str] = Field(description=c.MINUTE)
    hour: Optional[str] = Field(description=c.HOUR)
    day: Optional[str] = Field(description=c.DAY)
    week: Optional[str] = Field(description=c.WEEK)
    day_of_week: Optional[str] = Field(description=c.DAY_OF_WEEK)
    month: Optional[str] = Field(description=c.MONTH)
    year: Optional[str] = Field(description=c.YEAR)

    @validator("end_date")
    def start_date_before_end_date(cls, v, values):
        if v and values["start_date"] and v < values["start_date"]:
            raise ValueError("end_date should not be before start_date")
        return v

    @validator(
        "year", "month", "day_of_week", "week", "day", "hour", "minute", "second"
    )
    def valid_expressions(cls, v, field):
        fields_map = {
            "year": BaseField,
            "month": MonthField,
            "week": WeekField,
            "day": DayOfMonthField,
            "day_of_week": DayOfWeekField,
            "hour": BaseField,
            "minute": BaseField,
            "second": BaseField,
        }
        field_class = fields_map[field.name]
        field_class(field.name, v, False)

        return v


class DateTrigger(BaseModel):
    class Config:
        title = "Date"

    trigger: Literal["date"]
    run_date: Union[datetime] = Field(description=c.RUN_DATE)


class Schedule(BaseModel):
    class Config:
        extra = Extra.forbid

    trigger: Union[CronTrigger, IntervalTrigger, DateTrigger] = Field(
        discriminator="trigger"
    )
    misfire_grace_time: Optional[int] = Field(
        default=300, description=c.MISFIRE_GRACE_TIME
    )
    max_instances: Optional[int] = Field(default=1, description=c.MAX_INSTANCES)
