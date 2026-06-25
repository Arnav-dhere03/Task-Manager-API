from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

from app.models.task import (
    TaskStatus,
    TaskPriority
)


class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=150
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    priority: TaskPriority = TaskPriority.MEDIUM

    due_date: Optional[datetime] = None

    project_id: Optional[int] = None

    assigned_user_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=150
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    status: Optional[TaskStatus] = None

    priority: Optional[TaskPriority] = None

    due_date: Optional[datetime] = None

    assigned_user_id: Optional[int] = None


class TaskResponse(BaseModel):
    id: int

    title: str
    description: Optional[str]

    status: TaskStatus
    priority: TaskPriority

    due_date: Optional[datetime]

    project_id: Optional[int]

    creator_id: int
    assigned_user_id: Optional[int]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None

    priority: Optional[TaskPriority] = None

    project_id: Optional[int] = None

    assigned_user_id: Optional[int] = None