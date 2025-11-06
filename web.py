from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os


router = APIRouter()


BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


