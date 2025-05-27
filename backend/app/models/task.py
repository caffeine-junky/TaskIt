from uuid import uuid4, UUID
from sqlmodel import Field, SQLModel
from pydantic import Field as PField, BaseModel
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from enum import StrEnum


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(max_length=1000, nullable=True)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.LOW)
    due_date: Optional[datetime] = Field(nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskCreate(BaseModel):
    title: str = PField(max_length=100)
    description: str = PField(max_length=1000)
    priority: TaskPriority
    due_date: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "title": "Task title",
                "description": "Task description",
                "priority": "low",
                "due_date": "2025-06-01T00:00:00Z",
            }
        }


class TaskUpdate(BaseModel):
    title: Optional[str] = PField(max_length=100, default=None)
    description: Optional[str] = PField(max_length=1000, default=None)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "title": "Task title",
                "description": "Task description",
                "status": "pending",
                "priority": "low",
                "due_date": "2025-06-01T00:00:00Z",
            }
        }
