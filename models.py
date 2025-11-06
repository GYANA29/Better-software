from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False, index=True)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

	comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")


class Comment(Base):
	__tablename__ = "comments"

	id = Column(Integer, primary_key=True, index=True)
	task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
	content = Column(Text, nullable=False)
	author = Column(String(100), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

	task = relationship("Task", back_populates="comments")


