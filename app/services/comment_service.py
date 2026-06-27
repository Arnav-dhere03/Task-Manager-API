from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.models.task import Task

from app.schemas.comment import (
    CommentCreate,
    CommentUpdate
)


def get_comment_by_id(
    db: Session,
    comment_id: int
):
    return (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )


def get_task_comments(
    db: Session,
    task_id: int
):
    return (
        db.query(Comment)
        .filter(Comment.task_id == task_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


def create_comment(
    db: Session,
    task: Task,
    comment_data: CommentCreate,
    user_id: int
):
    comment = Comment(
        content=comment_data.content,
        task_id=task.id,
        user_id=user_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def update_comment(
    db: Session,
    comment: Comment,
    comment_data: CommentUpdate
):
    update_data = comment_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(comment, field, value)

    db.commit()
    db.refresh(comment)

    return comment


def delete_comment(
    db: Session,
    comment: Comment
):
    db.delete(comment)
    db.commit()


def is_comment_owner(
    comment: Comment,
    user_id: int
):
    return comment.user_id == user_id