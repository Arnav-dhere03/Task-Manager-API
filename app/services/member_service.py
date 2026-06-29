from sqlalchemy.orm import Session

from app.models.user import User
from app.models.project import Project
from app.services.activity_service import log_activity
from app.models.activity import (
    ActivityAction,
    EntityType
)

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def add_member_to_project(
    db: Session,
    project: Project,
    user: User,
    user_id: int
):
    if user not in project.members:
        project.members.append(user)

        db.commit()
        db.refresh(project)
        log_activity(
            db=db,
            user_id=user_id,
            action=ActivityAction.ADD_MEMBER,
            entity_type=EntityType.PROJECT,
            entity_id=project.id,
            project_id=project.id,
            description=f"Added {user.username} to project"
        )
        db.commit()
    return project

def remove_member_from_project(
    db: Session,
    project: Project,
    user: User,
    user_id: int
):
    if user in project.members:
        project.members.remove(user)

        db.commit()
        db.refresh(project)
        log_activity(
            db=db,
            user_id=user_id,
            action=ActivityAction.REMOVE_MEMBER,
            entity_type=EntityType.PROJECT,
            entity_id=project.id,
            project_id=project.id,
            description=f"Removed {user.username} from project"
        )
        db.commit()
    return project

def get_project_members(
    project: Project
):
    return project.members