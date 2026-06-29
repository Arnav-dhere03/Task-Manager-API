from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies.auth_dependency import (
    get_current_user
)
from app.schemas.member import (
    AddMemberRequest,
    MemberResponse
)
from app.services.project_service import (
    get_project_by_id,
    is_project_owner,
    is_project_member
)
from app.services.member_service import (
    get_user_by_email,
    add_member_to_project,
    remove_member_from_project,
    get_project_members
)
router = APIRouter(
    prefix="/projects",
    tags=["Project Members"]
)

@router.post(
    "/{project_id}/members",
    response_model=list[MemberResponse]
)
def add_member(
    project_id: int,
    request: AddMemberRequest,
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

    if not is_project_owner(
        project,
        current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only project owner can add members"
        )

    user = get_user_by_email(
        db,
        request.email
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    add_member_to_project(
        db,
        project,
        user,
        current_user.id
    )

    return get_project_members(project)

@router.get(
    "/{project_id}/members",
    response_model=list[MemberResponse]
)
def view_members(
    project_id: int,
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

    owner = is_project_owner(
        project,
        current_user.id
    )

    member = is_project_member(
        project,
        current_user.id
    )

    if not owner and not member:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return get_project_members(project)

@router.delete(
    "/{project_id}/members/{user_id}",
    response_model=list[MemberResponse]
)
def remove_member(
    project_id: int,
    user_id: int,
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

    if not is_project_owner(
        project,
        current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only project owner can remove members"
        )

    member = next(
        (
            m for m in project.members
            if m.id == user_id
        ),
        None
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    remove_member_from_project(
        db,
        project,
        member,
        current_user.id
    )

    return get_project_members(project)