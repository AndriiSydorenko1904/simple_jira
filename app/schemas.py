from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.config import TaskStatus, TaskPriority


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    assigned_to: int


class TaskUpdate(TaskBase):
    status: Optional[TaskStatus] = None


class TaskRead(TaskBase):
    id: int
    owner_id: int
    assigned_to: int

    class Config:
        from_attributes = True
