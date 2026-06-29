from sqlalchemy.orm import Session

from app.models.activity import (
    Activity,
    ActivityAction,
    EntityType
)


def log_activity(
    db: Session,
    *,
    user_id: int,
    action: ActivityAction,
    entity_type: EntityType,
    entity_id: int,
    description: str,
    project_id: int | None = None
):
    activity = Activity(
        user_id=user_id,
        project_id=project_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description
    )

    db.add(activity)
    return activity


def get_project_activities(
    db: Session,
    project_id: int,
    page: int = 1,
    size: int = 20
):
    query = (
        db.query(Activity)
        .filter(Activity.project_id == project_id)
    )

    total = query.count()

    pages = (total + size - 1) // size

    activities = (
        query
        .order_by(Activity.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {
        "items": activities,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


def get_user_activities(
    db: Session,
    user_id: int,
    page: int = 1,
    size: int = 20
):
    query = (
        db.query(Activity)
        .filter(Activity.user_id == user_id)
    )

    total = query.count()

    pages = (total + size - 1) // size

    activities = (
        query
        .order_by(Activity.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {
        "items": activities,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }