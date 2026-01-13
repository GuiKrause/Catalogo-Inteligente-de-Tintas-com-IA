from fastapi import FastAPI
from .core.database import Base, engine
from .routers import auth, users, paints

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(paints.router)