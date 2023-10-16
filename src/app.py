import sys
sys.path.append("../KongBot/")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

import uvicorn

from routes.graph.route import router as graph_router
from routes.auth.route import router as auth_router
from routes.events.route import router as events_router
from routes.static.route import router as static_router

from common.message_queue.queue import KafkaQueue

app = FastAPI()

# Set up the CORS middleware
origins = [
    "http://localhost:3000",  # Allow requests from your local frontend
    "http://localhost:5900",
    "http://localhost:10559"
    # Add any other origins (frontend URLs) you want to allow
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


@app.get("/")
def read_root():
    with open(os.path.join(STATIC_DIR, "index.html"), 'r') as f:
        content = f.read()
        return HTMLResponse(content=content)


app.include_router(graph_router)
app.include_router(auth_router)
app.include_router(events_router)

app.queue = KafkaQueue()
# realistically, needs to be a dictionary keyed by user IDs
app.curr_graph = None

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
