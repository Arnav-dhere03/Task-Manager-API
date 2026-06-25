from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

project_members = Table(
    "project_members",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    )
)