from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate
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
    project_data: ProjectUpdate
):
    if project_data.name is not None:
        project.name = project_data.name

    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project: Project
):
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