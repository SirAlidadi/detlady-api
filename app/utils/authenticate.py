from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.UsersModel import Users
from app.schemas.UsersSchema import AuthUserSchema
from app.utils.bcrypt import Bcrypt
from app.services.UsersManager import get as orm_get_user
from app.utils.exceptions import login_exception


SECRET_KEY = "5ad201d0812bf4b355005426162e69896332291e420be45d09b1dd5d266b2685"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(phone: str, password: str, db: Session):
    user = db.query(Users).filter(Users.phone == phone).first()
    if not user:
        return False
    if not Bcrypt.verify_bcrypt(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        
        if id is None:
            raise login_exception("حساب کاربری شما توسط سیستم تایید نشد.")

    except JWTError:
        raise login_exception("حساب کاربری شما توسط سیستم تایید نشد.")

    user = orm_get_user(id, db)
    
    if user is None:
        raise login_exception("حساب کاربری شما توسط سیستم تایید نشد.")

    return user


def current_active_user(current_user: Annotated[AuthUserSchema, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="حساب کابری شما غیر فعال می باشد.")
    return current_user


def current_admin_user(current_user: Annotated[AuthUserSchema, Depends(get_current_user)]):
    if not current_user.is_active or not current_user.is_admin:
        raise HTTPException(status_code=400, detail="حساب کاربری شما برای مجاز به انجام این عملیات نمی باشد")
    return current_user
