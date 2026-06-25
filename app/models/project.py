from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.project_members import project_members


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

    # Owner/Admin of project
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Owner relationship
    owner = relationship(
        "User",
        back_populates="owned_projects"
    )

    # Collaborative members
    members = relationship(
        "User",
        secondary=project_members,
        back_populates="collaborative_projects"
    )

    # Tasks under project
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete"
    )