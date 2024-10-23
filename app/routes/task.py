from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.schemas import TaskCreate, TaskUpdate, TaskRead
from app.models import Task, User
from app.database import get_db
from app.services import on_task_status_change
from app.utils import get_admin_or_manager, get_admin, get_admin_or_manager_or_user


task_router = APIRouter()


@cbv(task_router)
class TaskRoutes:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    @task_router.post("/tasks/", response_model=TaskCreate)
    def create_task(self, task: TaskCreate, current_user: User = Depends(get_admin_or_manager)):
        new_task = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            assigned_to=task.assigned_to,
            owner_id=current_user.id
        )

        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    @task_router.get("/tasks/", response_model=List[TaskRead])
    def get_tasks(self, current_user: User = Depends(get_admin_or_manager_or_user)):
        tasks = self.db.query(Task).all()
        return tasks

    @task_router.get("/tasks/{task_id}", response_model=TaskRead)
    def get_task(self, task_id: int, current_user: User = Depends(get_admin_or_manager_or_user)):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @task_router.get("/my-tasks/", response_model=List[TaskRead])
    def get_my_tasks(self, current_user: User = Depends(get_admin_or_manager_or_user)):
        tasks = self.db.query(Task).filter(Task.assigned_to == current_user.id).all()
        return tasks

    @task_router.put("/tasks/{task_id}", response_model=TaskUpdate)
    def update_task(self, task_id: int, task: TaskUpdate, current_user: User = Depends(get_admin_or_manager_or_user)):
        db_task = self.db.query(Task).filter(Task.id == task_id).first()

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        db_task.title = task.title or db_task.title
        db_task.description = task.description or db_task.description
        db_task.priority = task.priority or db_task.priority
        db_task.status = task.status or db_task.status

        if task.status:
            on_task_status_change(db_task)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    @task_router.delete("/tasks/{task_id}")
    def delete_task(self, task_id: int, current_user: User = Depends(get_admin)):
        db_task = self.db.query(Task).filter(Task.id == task_id).first()

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        self.db.delete(db_task)
        self.db.commit()
        return {"detail": "Task deleted"}
