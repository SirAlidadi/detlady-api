from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.models import UsersModel
from app.config.database import engine
from .routers import UsersRouter


disable_installed_extensions_check()

app = FastAPI()
add_pagination(app)
app.include_router(UsersRouter.router)

UsersModel.Base.metadata.create_all(bind=engine)