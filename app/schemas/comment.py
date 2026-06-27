from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)

class CommentUser(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )

class CommentBase(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500
    )

class CommentResponse(BaseModel):
    id: int
    content: str
    task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: CommentUser

    model_config = ConfigDict(
        from_attributes=True
    )