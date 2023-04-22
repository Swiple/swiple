import json
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import Extra, validator
from app.models.base_model import BaseModel


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    RETRY = "RETRY"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class Result(BaseModel):
    dataset_id: Optional[str]
    datasource_id: Optional[str]
    exc_message: Optional[list[str]]
    exc_module: Optional[str]
    exc_type: Optional[str]

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        _ignored = kwargs.pop('exclude_none')
        return super().dict(*args, exclude_none=True, **kwargs)

    class Config:
        extra = Extra.ignore


class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus
    kwargs: Optional[dict]
    result: Optional[Result]
    name: Optional[str]
    retries: Optional[int]
    date_done: Optional[datetime]

    @validator('result', pre=True)
    def ensure_result_is_dict(cls, value):
        if value is None:
            return None
        elif isinstance(value, dict):
            return value
        elif isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string for 'result' field")
        else:
            raise ValueError("Invalid value for 'result' field")

    class Config:
        extra = Extra.ignore


class TaskResultResponse(TaskResult):
    pass


class TaskReadyResponse(BaseModel):
    is_ready: bool


class TaskIdResponse(BaseModel):
    task_id: str


class Task(BaseModel):
    result: TaskResult
    timestamp: str
