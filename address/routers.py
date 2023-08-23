from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from .schemas import BaseAddressSchema, UpdateAddressSchema
from customer.schemas import AuthUserSchema
from core.authenticate import current_active_user
from .managers import address_manager


router = APIRouter(prefix='/address', tags=["Address"])


@router.post('/create', response_model=BaseAddressSchema)
def create_address(
    request: BaseAddressSchema,
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db)
):
    return address_manager.create(data=request.model_dump(), user_id=current_user.id, db=db)


@router.get('/', name="get all addresses for user")
def get_address(
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db),
):
    return address_manager.get_all(user_id=current_user.id, db=db)


@router.delete('/delete/{id}')
def delete_address(
    id: int,
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db)
):
    return address_manager.delete(id, user_id=current_user.id, db=db)


@router.patch('/update/{id}')
def update_address(
    request: UpdateAddressSchema,
    id: int,
    current_user: Annotated[AuthUserSchema, Depends(current_active_user)],
    db: Session = Depends(get_db)
):
    return address_manager.update(
        data=request.model_dump(exclude_unset=True),
        id=id,
        user_id=current_user.id,
        db=db
    )
