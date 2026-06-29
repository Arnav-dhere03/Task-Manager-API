from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate
)
from app.services.activity_service import log_activity
from app.models.activity import (
    ActivityAction,
    EntityType
)

def create_project(
    db: Session,
    project_data: ProjectCreate,
    owner_id: int
):
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    log_activity(
        db=db,
        user_id=owner_id,
        action=ActivityAction.CREATE,
        entity_type=EntityType.PROJECT,
        entity_id=new_project.id,
        project_id=new_project.id,
        description=f"Created project '{new_project.name}'"
    )

    db.commit()
    return new_project


def get_user_projects(
    db: Session,
    user_id: int
):
    return db.query(Project).filter(
        Project.owner_id == user_id
    ).all()


def get_project_by_id(
    db: Session,
    project_id: int
):
    return db.query(Project).filter(
        Project.id == project_id
    ).first()


def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
    user_id: int
):
    if project_data.name is not None:
        project.name = project_data.name

    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)
    log_activity(
        db=db,
        user_id=user_id,
        action=ActivityAction.UPDATE,
        entity_type=EntityType.PROJECT,
        entity_id=project.id,
        project_id=project.id,
        description=f"Updated project '{project.name}'"
    )

    db.commit()
    db.refresh(project)
    return project


def delete_project(
    db: Session,
    project: Project,
    user_id: int
):
    log_activity(
        db=db,
        user_id=user_id,
        action=ActivityAction.DELETE,
        entity_type=EntityType.PROJECT,
        entity_id=project.id,
        project_id=project.id,
        description=f"Deleted project '{project.name}'"
    )

    db.delete(project)
    db.commit()


def is_project_owner(
    project: Project,
    user_id: int
) -> bool:
    return project.owner_id == user_id

def is_project_member(
    project: Project,
    user_id: int
) -> bool:
    return any(
        member.id == user_id
        for member in project.members
    )

def can_access_project(
    project,
    user_id: int
) -> bool:
    
    return (
        is_project_owner(project, user_id)
        or is_project_member(project, user_id)
    )