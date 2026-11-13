
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str
    priority: TaskPriority
    status: TaskStatus = TaskStatus.TODO
    due_date: date


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    due_date: date | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    due_date: date
    created_at: datetime
    updated_at: datetime
