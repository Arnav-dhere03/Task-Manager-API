from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.task import Task,TaskPriority,TaskStatus
from app.models.project import Project
from app.models.user import User
from app.services.project_service import (
    is_project_owner,
    is_project_member
)
from app.schemas.task import (
    TaskCreate,
    TaskUpdate
)

def get_task_by_id(
    db: Session,
    task_id: int
):
    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

def create_task(
    db: Session,
    task_data: TaskCreate,
    creator_id: int
):
    if task_data.project_id is not None:

        project = (
            db.query(Project)
            .filter(Project.id == task_data.project_id)
            .first()
        )

        if not project:
            raise ValueError("Project not found")

        creator = (
            db.query(User)
            .filter(User.id == creator_id)
            .first()
        )

        if creator is None:
            raise ValueError("Creator not found")

        if not (
            is_project_owner(project, creator_id)
            or is_project_member(project, creator_id)
        ):
            raise ValueError(
                "You are not a member of this project."
            )

        if task_data.assigned_user_id is not None:

            assignee = (
                db.query(User)
                .filter(User.id == task_data.assigned_user_id)
                .first()
            )

            if assignee is None:
                raise ValueError("Assigned user not found")

            if not (
                is_project_owner(project, assignee.id)
                or is_project_member(project, assignee.id)
            ):
                raise ValueError(
                    "Assigned user is not a member of this project."
                )

    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        project_id=task_data.project_id,
        creator_id=creator_id,
        assigned_user_id=task_data.assigned_user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_user_tasks(
    db: Session,
    user_id: int
):
    return (
        db.query(Task)
        .filter(
            (Task.creator_id == user_id)
            |
            (Task.assigned_user_id == user_id)
        )
        .distinct()
        .all()
    )

def get_project_tasks(
    db: Session,
    project_id: int
):
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .all()
    )

def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate
):
    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            task,
            field,
            value
        )

    db.commit()
    db.refresh(task)

    return task

def delete_task(
    db: Session,
    task: Task
):
    db.delete(task)
    db.commit()

def can_access_task(
    task: Task,
    user_id: int
):
    if task.project is None:
        return (
            task.creator_id == user_id
            or task.assigned_user_id == user_id
        )

    if is_project_owner(task.project, user_id):
        return True

    if is_project_member(task.project, user_id):
        return True

    return (
        task.creator_id == user_id
        or task.assigned_user_id == user_id
    )

def can_assign_user_to_project_task(
    project: Project,
    user: User
):
    if project.owner_id == user.id:
        return True

    return user in project.members

def get_filtered_tasks(
    db: Session,
    user_id: int,
    status=None,
    priority=None,
    project_id=None,
    page: int = 1,
    size: int = 10
):
    query = db.query(Task).filter(
        (Task.creator_id == user_id)
        |
        (Task.assigned_user_id == user_id)
    )

    if status:
        query = query.filter(
            Task.status == status
        )

    if priority:
        query = query.filter(
            Task.priority == priority
        )

    if project_id:
        query = query.filter(
            Task.project_id == project_id
        )

    total = query.count()

    pages = (
        total + size - 1
    ) // size

    offset = (
        page - 1
    ) * size

    items = (
        query
        .offset(offset)
        .limit(size)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }