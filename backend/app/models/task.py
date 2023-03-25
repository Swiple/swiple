import os
from dotenv import load_dotenv
# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../../../docker/.env-local')
load_dotenv(dotenv_path)

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

from pydantic import Extra

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

    class Config:
        extra = Extra.ignore


class TaskResultResponse(TaskResult):
    pass


class TaskReadyResponse(BaseModel):
    is_ready: bool


class TaskIdResponse(BaseModel):
    task_id: str
