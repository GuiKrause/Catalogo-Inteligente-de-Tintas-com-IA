from fastapi import FastAPI
from .router import router as agent_router
from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

app.include_router(agent_router, tags=["Agente"])