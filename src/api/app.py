from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from src.api.dependencies import Dependencies
from src.api.auth.routes import router as auth_router
from src.config import settings
from src.repositories.users.abc import AbstractUserRepository
from src.repositories.users.repository import SqlUserRepository
from src.storage.sql import SQLAlchemyStorage

app = FastAPI()


async def setup_repositories():
    # ------------------- Repositories Dependencies -------------------
    storage = SQLAlchemyStorage.from_url(settings.DB_URL)
    user_repository = SqlUserRepository(storage)
    Dependencies.register_provider(AbstractUserRepository, user_repository)
    # await storage.drop_all()
    # await storage.create_all()


@app.on_event("startup")
async def startup_event():
    await setup_repositories()


# Redirect root to docs
@app.get("/", tags=["Root"], include_in_schema=False)
async def redirect_to_docs(request: Request):
    return RedirectResponse(url=request.url_for("swagger_ui_html"))


app.include_router(auth_router)
