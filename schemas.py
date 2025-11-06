from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
	title: str = Field(min_length=1, max_length=255)


class TaskCreate(TaskBase):
	pass


class TaskRead(TaskBase):
	id: int
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class CommentBase(BaseModel):
	content: str = Field(min_length=1)
	author: str = Field(min_length=1, max_length=100)


class CommentCreate(CommentBase):
	pass


class CommentUpdate(BaseModel):
	content: Optional[str] = Field(default=None, min_length=1)
	author: Optional[str] = Field(default=None, min_length=1, max_length=100)


class CommentRead(CommentBase):
	id: int
	task_id: int
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


