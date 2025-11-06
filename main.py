from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from .routers import comments, tasks
from . import web


def create_app() -> FastAPI:
	app = FastAPI(title="Task Comments API")

	# Allow local dev origins (Vite default and common localhost ports)
	app.add_middleware(
		CORSMiddleware,
		allow_origins=[
			"http://localhost:5173",
			"http://127.0.0.1:5173",
		],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
	app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
	app.include_router(comments.router, tags=["comments"])  # includes nested under /tasks and direct /comments

	# Mount static files (JS/CSS)
	app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

	# Web UI
	app.include_router(web.router)

	# Simple health check
	health = APIRouter()

	@health.get("/health")
	def health_check():
		return {"status": "ok"}

	app.include_router(health, tags=["health"])
	return app


app = create_app()


