from sqlalchemy.orm import Session

from app.models.user import User
from app.models.project import Project

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
    user: User
):
    if user not in project.members:
        project.members.append(user)

        db.commit()
        db.refresh(project)

    return project

def remove_member_from_project(
    db: Session,
    project: Project,
    user: User
):
    if user in project.members:
        project.members.remove(user)

        db.commit()
        db.refresh(project)

    return project

def get_project_members(
    project: Project
):
    return project.members