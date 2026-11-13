
from fastapi import FastAPI

from backend.app.routes.task import router as task_router
from backend.app.routes.auth import router as auth_router

app = FastAPI(
    title="UniTask API",
    description="API REST de gestion des tâches avec authentification JWT",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
def home():
    return {"message": "Bienvenue sur UniTask API"}

