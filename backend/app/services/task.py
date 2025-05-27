from uuid import UUID
# from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Optional, List
from app.models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from app.database import Database


class TaskService:
    """
    """
    
    def __init__(self, db: Database) -> None:
        self.db = db
    
    async def create(self, data: TaskCreate) -> Task:
        """"""
        session: Session = next(self.db.session)
        task: Task = Task(**data.model_dump())
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
    async def get(self, task_id: UUID) -> Task:
        """"""
        session: Session = next(self.db.session)
        task: Optional[Task] = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
    async def update(self, task_id: UUID, data: TaskUpdate) -> Task:
        """"""
        session: Session = next(self.db.session)
        task: Optional[Task] = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        session.commit()
        session.refresh(task)
        return task
    
    async def delete(self, task_id: UUID) -> None:
        """"""
        session: Session = next(self.db.session)
        task: Optional[Task] = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()

    async def getall(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None
        ) -> List[Task]:
        """"""
        session: Session = next(self.db.session)
        query = select(Task)

        if status is not None: query = query.where(Task.status == status)
        if priority is not None: query = query.where(Task.priority == priority)
        if skip is not None: query = query.offset(skip)
        if limit is not None: query = query.limit(limit)

        tasks: List[Task] = list(session.exec(select(Task)).all())
        return tasks
