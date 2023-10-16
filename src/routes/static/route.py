from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

STATIC_DIR = "build"


