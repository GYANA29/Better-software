import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import create_app
from backend.app.database import Base, get_db


TEST_DB_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator[None, None, None]:
	# Fresh test database file
	if os.path.exists("test.db"):
		os.remove("test.db")
	yield
	# On Windows, SQLite file can remain locked briefly. Best-effort cleanup.
	if os.path.exists("test.db"):
		try:
			os.remove("test.db")
		except PermissionError:
			pass


@pytest.fixture()
def client() -> TestClient:
	engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
	TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

	# Create tables
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)

	app = create_app()

	def override_get_db():
		db = TestingSessionLocal()
		try:
			yield db
		finally:
			db.close()

	app.dependency_overrides[get_db] = override_get_db
	return TestClient(app)


def test_comment_crud_flow(client: TestClient):
	# Create a task
	resp = client.post("/tasks/", json={"title": "Test Task"})
	assert resp.status_code == 201, resp.text
	task = resp.json()
	task_id = task["id"]

	# Initially no comments
	resp = client.get(f"/tasks/{task_id}/comments")
	assert resp.status_code == 200
	assert resp.json() == []

	# Create a comment
	payload = {"content": "First!", "author": "alice"}
	resp = client.post(f"/tasks/{task_id}/comments", json=payload)
	assert resp.status_code == 201, resp.text
	comment = resp.json()
	comment_id = comment["id"]
	assert comment["task_id"] == task_id
	assert comment["content"] == "First!"
	assert comment["author"] == "alice"

	# List shows the created one
	resp = client.get(f"/tasks/{task_id}/comments")
	assert resp.status_code == 200
	comments = resp.json()
	assert len(comments) == 1
	assert comments[0]["id"] == comment_id

	# Get single
	resp = client.get(f"/comments/{comment_id}")
	assert resp.status_code == 200

	# Update partial
	resp = client.patch(f"/comments/{comment_id}", json={"content": "Edited"})
	assert resp.status_code == 200
	assert resp.json()["content"] == "Edited"

	# Delete
	resp = client.delete(f"/comments/{comment_id}")
	assert resp.status_code == 204

	# Now 404
	resp = client.get(f"/comments/{comment_id}")
	assert resp.status_code == 404

	# Listing is empty again
	resp = client.get(f"/tasks/{task_id}/comments")
	assert resp.status_code == 200
	assert resp.json() == []


def test_create_comment_on_missing_task_returns_404(client: TestClient):
	resp = client.post("/tasks/9999/comments", json={"content": "x", "author": "a"})
	assert resp.status_code == 404


