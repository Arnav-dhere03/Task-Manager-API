from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    content = Column(
        String(500),
        nullable=False
    )
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
    task_id = Column(
        Integer,
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE"
        ),
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
    task = relationship(
        "Task",
        back_populates="comments"
    )
    user = relationship(
        "User",
        back_populates="comments"
    )