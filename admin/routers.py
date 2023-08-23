from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from core.authenticate import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from core.exceptions import login_exception


router = APIRouter(tags=["Admin"])

@router.post('/login')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(phone=form_data.username, password=form_data.password, db=db)
    
    if not user:
        raise login_exception()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"id": user.id},
        expires_delta=access_token_expires
    )
    
    if(user.is_admin):
        return {
            "id": user.id,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "access_token": access_token,
            "token_type": "bearer"
        }

    return {
        "id": user.id,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "access_token": access_token,
        "token_type": "bearer"
    }