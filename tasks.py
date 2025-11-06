from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db, Base, engine
from ..models import Task
from ..schemas import TaskCreate, TaskRead


# Ensure tables exist at import (simple demo). In production, use migrations.
Base.metadata.create_all(bind=engine)


router = APIRouter()


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
	task = Task(title=payload.title)
	db.add(task)
	db.commit()
	db.refresh(task)
	return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
	task = db.get(Task, task_id)
	if not task:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
	return task


