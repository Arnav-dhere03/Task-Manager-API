from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.project_members import project_members


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Projects owned by the user
    owned_projects = relationship(
        "Project",
        back_populates="owner",
        cascade="all, delete"
    )

    # Projects user collaborates in
    collaborative_projects = relationship(
        "Project",
        secondary=project_members,
        back_populates="members"
    )

    # Tasks created by user
    created_tasks = relationship(
        "Task",
        foreign_keys="Task.creator_id",
        back_populates="creator"
    )

    # Tasks assigned to user
    assigned_tasks = relationship(
        "Task",
        foreign_keys="Task.assigned_user_id",
        back_populates="assigned_user"
    )

    # Comments by user
    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete"
    )