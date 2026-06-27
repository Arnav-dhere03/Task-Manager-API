from fastapi import FastAPI
from app.routers import auth_router, project_member_router,projects,task_router,comment_router
from app.models import (
    User,
    Project,
    Task,
    Comment,
    project_members
)

app = FastAPI(
    title="Task Manager API",
    description="Resume-level FastAPI backend for task management, collaboration, and productivity",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Task Manager API is running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

app.include_router(auth_router.router)
app.include_router(projects.router)
app.include_router(project_member_router.router)
app.include_router(task_router.router)
app.include_router(comment_router.router)