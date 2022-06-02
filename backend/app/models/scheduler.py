from app.models.base_model import BaseModel
from typing import Literal, List, Union, Optional
from datetime import datetime


class IntervalTrigger(BaseModel):
    start_date: Optional[Union[datetime, str]]
    end_date: Optional[Union[datetime, str]]
    seconds: Union[int, str]
    minutes: Union[int, str]
    hours: Union[int, str]
    weeks: Union[int, str]


class CronTrigger(BaseModel):
    start_date: Optional[Union[datetime, str]]
    end_date: Optional[Union[datetime, str]]
    second: Union[int, str]
    minute: Union[int, str]
    hour: Union[int, str]
    day_of_week: Union[int, str]
    week: Union[int, str]
    month: Union[int, str]
    year: Union[int, str]


class DateTrigger(BaseModel):
    run_date: Union[datetime, str]


class Job(BaseModel):
    func: any
    trigger: Literal["interval", "cron", "date"]
    args: List[IntervalTrigger, CronTrigger, DateTrigger]

