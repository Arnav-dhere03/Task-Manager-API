from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict
)

from app.models.activity import (
    ActivityAction,
    EntityType
)


class ActivityUser(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ActivityProject(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ActivityResponse(BaseModel):
    id: int

    action: ActivityAction

    entity_type: EntityType

    entity_id: int

    description: str

    created_at: datetime

    user: ActivityUser

    project: ActivityProject | None = None

    model_config = ConfigDict(
        from_attributes=True
    )