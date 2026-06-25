from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import enum

from app.database import Base

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(Base):
    __tablename__ = "tasks"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Basic Information
    title = Column(
        String(150),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    # Task State
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.TODO,
        nullable=False
    )

    priority = Column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM,
        nullable=False
    )

    # Deadline
    due_date = Column(
        DateTime,
        nullable=True
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Optional Project
    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )

    # Creator
    creator_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # Assigned User
    assigned_user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    # Parent Project
    project = relationship(
        "Project",
        back_populates="tasks"
    )

    # User who created task
    creator = relationship(
        "User",
        foreign_keys=[creator_id],
        back_populates="created_tasks"
    )

    # User assigned task
    assigned_user = relationship(
        "User",
        foreign_keys=[assigned_user_id],
        back_populates="assigned_tasks"
    )

    # Task comments
    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan"
    )