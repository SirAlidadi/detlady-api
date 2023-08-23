from typing import Annotated, List, Optional
from fastapi import Depends, Path, Response, status
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from core.database import get_db
from .schemas import CreateUserSchema, DeleteUsersSchema, DisplayUserSchema, UpdateUserSchema
from fastapi_pagination import Page, paginate
from .managers import user_manager



router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    '/create',
    response_model=DisplayUserSchema
)
def create_user(request: CreateUserSchema, response: Response, db: Session = Depends(get_db)):
    instance = user_manager.create(request, db)
    response.status_code = status.HTTP_201_CREATED
    return instance


@router.get(
    '/',
    response_model=Page[DisplayUserSchema]
)
def list_user(
    search: Annotated[str | None, Optional[Path(min_length=1)]] = None,
    db: Session = Depends(get_db)
):
    instance = user_manager.get_all(db=db, search=search)
    return paginate(instance)


@router.get(
    '/{id}',
    response_model=DisplayUserSchema
)
def get_user(
    id: int,
    db: Session = Depends(get_db)
):
    return user_manager.get(id=id, db=db)


@router.delete('/delete/')
def delete_users(
    ids: DeleteUsersSchema,
    db: Session = Depends(get_db)
):
    return user_manager.deleteAll(items=ids, db=db)


@router.patch(
    '/update/{id}',
    response_model=DisplayUserSchema
)
def update_user(
    request: UpdateUserSchema,
    id: int,
    db: Session = Depends(get_db)
):
    return user_manager.update(
        data=request.model_dump(exclude_unset=True, exclude_none=True),
        id=id,
        db=db
    )
