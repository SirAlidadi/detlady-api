from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.models import AddressModel, UsersModel
from app.config.database import engine
from .routers import UsersRouter, AddressRouter, AuthenticateRouter


app = FastAPI()


app.include_router(UsersRouter.router)
app.include_router(AddressRouter.router)
app.include_router(AuthenticateRouter.router)

UsersModel.Base.metadata.create_all(bind=engine)
AddressModel.Base.metadata.create_all(bind=engine)

add_pagination(app)

disable_installed_extensions_check()
