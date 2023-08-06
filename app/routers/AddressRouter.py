from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.AddressSchema import BaseAddressSchema, UpdateAddressSchema
from app.schemas.UsersSchema import AuthUserSchema
from app.services.AddressManager import create as orm_create_address,\
                                        delete as orm_delete_address,\
                                        get as orm_get_address,\
                                        update as orm_update_address
from app.utils.authenticate import current_active_user
from app.utils.types import ID_TYPE

router = APIRouter(prefix='/address', tags=["Address"])


@router.post('/create', response_model=BaseAddressSchema)
def create_address(
    request: BaseAddressSchema,
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db)
):
    return orm_create_address(request, current_user, db)


@router.get('/', name="get all addresses for user")
def get_address(
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db),
):
    return orm_get_address(current_user, db)


@router.delete('/delete/{id}')
def delete_address(
    id: ID_TYPE,
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db)
):
    return orm_delete_address(id, current_user, db)


@router.patch('/update/{id}')
def update_address(
    request: UpdateAddressSchema,
    id: ID_TYPE,
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db)
):
    return orm_update_address(request, id, current_user, db)


