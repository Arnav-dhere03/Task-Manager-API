from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies.auth_dependency import get_current_user
from app.schemas.activity import ActivityResponse
from app.services.activity_service import (
    get_project_activities,
    get_user_activities
)
from app.services.project_service import (
    get_project_by_id,
    can_access_project
)
router = APIRouter(
    tags=["Activities"]
)

@router.get(
    "/projects/{project_id}/activities"
)
def project_activity_feed(
    project_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(
        db,
        project_id
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    if not can_access_project(
        project,
        current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    return get_project_activities(
        db=db,
        project_id=project.id,
        page=page,
        size=size
    )

@router.get(
    "/users/me/activities"
)
def my_activity_feed(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_activities(
        db=db,
        user_id=current_user.id,
        page=page,
        size=size
    )