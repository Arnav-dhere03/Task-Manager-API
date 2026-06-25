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

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)

from app.services.task_service import (
    create_task,
    get_task_by_id,
    get_user_tasks,
    get_project_tasks,
    update_task,
    delete_task,
    can_access_task
)

from app.services.project_service import (
    get_project_by_id,
    is_project_owner,
    is_project_member
)
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_task(
            db,
            task_data,
            current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_tasks(
        db,
        current_user.id
    )

@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
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

    return task

@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
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

    if task.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only creator can update task"
        )

    return update_task(
        db,
        task,
        task_data
    )

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_task(
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

    if task.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only creator can delete task"
        )

    delete_task(
        db,
        task
    )

    return None

@router.get(
    "/project/{project_id}",
    response_model=list[TaskResponse]
)
def get_tasks_for_project(
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

    return get_project_tasks(
        db,
        project_id
    )
