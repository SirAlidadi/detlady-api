from typing import List, Annotated, Optional
from fastapi import Depends, Path, Response, status
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from app.config.database import get_db
from app.schemas.UsersSchema import CreateUserSchema, DisplayUserSchema, UpdateUserSchema
from fastapi_pagination import Page, paginate

from app.services.UserManager import create as orm_create_user
from app.services.UserManager import list as orm_list_user
from app.services.UserManager import get as orm_get_user
from app.services.UserManager import delete as orm_delete_user
from app.services.UserManager import update as orm_update_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    '/create',
    response_model=DisplayUserSchema
)
def create_user(request: CreateUserSchema, response: Response, db: Session = Depends(get_db)):
    instance = orm_create_user(request, db)

    response.status_code = status.HTTP_201_CREATED
    return instance


@router.get(
    '/',
    response_model=Page[DisplayUserSchema]
)
def list_user(search: Annotated[str | None, Optional[Path(min_length=1)]] = None, db: Session = Depends(get_db)):
    instance = orm_list_user(search, db)
    return paginate(instance)


@router.get(
    '/{id}',
    response_model=DisplayUserSchema
)
def list_user(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    instance = orm_get_user(id, db)
    return instance


@router.delete(
    '/{id}',
    response_model=DisplayUserSchema
)
def delete_user(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    return orm_delete_user(id, db)


@router.patch(
    '/update/{id}',
    response_model=DisplayUserSchema
)
def update_user(request: UpdateUserSchema, id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    return orm_update_user(id, request, db)
