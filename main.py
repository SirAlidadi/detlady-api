from fastapi import FastAPI
from core.database import engine, Base
from fastapi_pagination import add_pagination
from fastapi.staticfiles import StaticFiles
from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi.middleware.cors import CORSMiddleware

from product import routers as product_router #, models as product_model
from customer import routers as customer_router #, models as customer_model
from address import routers as address_router #, models as address_model
from admin import routers as admin_router

app = FastAPI()

app.mount("/media", StaticFiles(directory="media/"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router.router)
app.include_router(customer_router.router)
app.include_router(address_router.router)
app.include_router(product_router.router)

Base.metadata.create_all(bind=engine)

add_pagination(app)

disable_installed_extensions_check()
