from uuid import UUID
from fastapi import APIRouter, Request, Depends
from typing import List, Optional
from app.database import Database
from app.models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from app.services import TaskService


router: APIRouter = APIRouter(prefix="/task", tags=["Task"])


async def get_db(request: Request) -> Database:
    """Get the database from the request"""
    return request.app.state.db


async def get_task_service(db: Database = Depends(get_db)) -> TaskService:
    """Get the task service"""
    return TaskService(db)


@router.post("/", response_model=Task, status_code=201)
async def create_task(
    data: TaskCreate,
    service: TaskService = Depends(get_task_service)
) -> Task:
    """Create a new task"""
    return await service.create(data)


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service)
) -> Task:
    """Get a task by id"""
    return await service.get(task_id)


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
) -> Task:
    """Update a task by id"""
    return await service.update(task_id, data)


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service)
) -> None:
    """Delete a task by id"""
    await service.delete(task_id)


@router.get("/", response_model=List[Task])
async def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    service: TaskService = Depends(get_task_service)
) -> List[Task]:
    """Get all tasks"""
    return await service.getall(status, priority, skip, limit)
