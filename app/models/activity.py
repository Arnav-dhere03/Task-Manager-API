import enum
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
from app.database import Base
class ActivityAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    ASSIGN = "assign"

    COMMENT = "comment"

    STATUS_CHANGE = "status_change"

    ADD_MEMBER = "add_member"
    REMOVE_MEMBER = "remove_member"

    LOGIN = "login"
    REGISTER = "register"

class EntityType(str, enum.Enum):
    PROJECT = "project"
    TASK = "task"
    COMMENT = "comment"
    USER = "user"

class Activity(Base):
    __tablename__ = "activities"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    action = Column(
        Enum(ActivityAction),
        nullable=False
    )

    entity_type = Column(
        Enum(EntityType),
        nullable=False
    )

    entity_id = Column(
        Integer,
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="activities"
    )

    project = relationship(
        "Project",
        back_populates="activities"
    )