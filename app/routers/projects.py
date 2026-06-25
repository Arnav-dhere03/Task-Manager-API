from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.dependencies.auth_dependency import get_current_user

from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)

from app.services.project_service import (
    create_project,
    get_user_projects,
    get_project_by_id,
    update_project,
    delete_project,
    is_project_owner
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_project(
        db,
        project_data,
        current_user.id
    )


@router.get(
    "",
    response_model=list[ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_projects(
        db,
        current_user.id
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(404, "Project not found")

    if not is_project_owner(project, current_user.id):
        raise HTTPException(403, "Not authorized")

    return project


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(404, "Project not found")

    if not is_project_owner(project, current_user.id):
        raise HTTPException(403, "Not authorized")

    return update_project(
        db,
        project,
        project_data
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(404, "Project not found")

    if not is_project_owner(project, current_user.id):
        raise HTTPException(403, "Not authorized")

    delete_project(db, project)