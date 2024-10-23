from fastapi import FastAPI
from app.routes.task import task_router
from app.routes.auth import auth_router

app = FastAPI(
    title="Task Tracker API",
    description="API for task tracker",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(task_router)
app.include_router(auth_router)
