from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import os
import uvicorn
from logging import getLogger
import yaml

from src.server.routes.graph.route import router as graph_router
from src.server.routes.auth.routes import router as auth_router
from src.server.routes.events.route import router as events_router
from src.server.routes.static.route import router as static_router

from src.server.utils.utils import log_start_banner

from config import settings


logger = getLogger("base")

log_start_banner()

app = FastAPI()

# TODO: add other configurations here, including database configurations
# log configurations done through yaml
# configure_logger(logger)


# Set up the CORS middleware
origins = [
    "http://localhost:3000",  # Allow requests from your local frontend
    "http://localhost:5900",
    "http://localhost:10559",
    "http://18.221.129.100:8000",
    "http://172.31.32.87:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = "build"
app.mount(
    "/static", StaticFiles(directory=os.path.join(STATIC_DIR, "static")))

# TODO: ideally we should delegate validation errors to a single error handler
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     logger.error("Request validation")
#     errors = {"errors": exc.errors()}
#     return HTTPException(status_code=400, detail="error")


@app.get("/")
def read_root():
    with open(os.path.join(STATIC_DIR, "index.html"), 'r') as f:
        content = f.read()
        return HTMLResponse(content=content)

app.include_router(graph_router)
app.include_router(auth_router)
app.include_router(events_router)

# realistically, needs to be a dictionary keyed by user IDs
app.curr_graph = None

# TODO: add linux yaml_config
with open(settings.LOG_CONFIG, "r") as config_file:
    yaml_config = yaml.safe_load(config_file.read())

if __name__ == "__main__":
    uvicorn.run("app:app", 
                host="0.0.0.0", 
                port=settings.API_PORT, 
                reload=True, 
                log_config=yaml_config)
