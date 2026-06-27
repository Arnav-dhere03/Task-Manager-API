from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies.auth_dependency import get_current_user
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse
)
from app.services.comment_service import (
    create_comment,
    get_comment_by_id,
    get_task_comments,
    update_comment,
    delete_comment,
    is_comment_owner
)
from app.services.task_service import (
    get_task_by_id,
    can_access_task
)
router = APIRouter(
    tags=["Comments"]
)

@router.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_comment(
    task_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(
        db,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    if not can_access_task(
        task,
        current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    
    return create_comment(
        db,
        task,
        comment_data,
        current_user.id
    )

@router.get(
    "/tasks/{task_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(
        db,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if not can_access_task(
        task,
        current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    return get_task_comments(
        db,
        task_id
    )

@router.patch(
    "/comments/{comment_id}",
    response_model=CommentResponse
)
def edit_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(
        db,
        comment_id
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )
    
    if not is_comment_owner(
        comment,
        current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own comments."
        )
    
    return update_comment(
        db,
        comment,
        comment_data
    )

@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(
        db,
        comment_id
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )
    
    if not is_comment_owner(
        comment,
        current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments."
        )
    delete_comment(
        db,
        comment
    )

    return None