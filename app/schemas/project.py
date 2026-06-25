from pydantic import BaseModel, Field
from typing import Optional


class ProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True