
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.UsersModel import Users
from app.schemas.UsersSchema import CreateUserSchema, UpdateUserSchema
from app.utils.bcrypt import Bcrypt


def create(user: CreateUserSchema, db: Session):
    user_exists = db.query(Users).filter(Users.phone == user.phone).first()
    if(user_exists):
        raise HTTPException(
            detail="There is a user with this phone number",
            status_code=status.HTTP_409_CONFLICT
        ) 
        
    query = Users()
    query.first_name = user.first_name
    query.last_name = user.last_name
    query.phone = user.phone
    query.password = Bcrypt.create_bcrypt(user.password)
    query.is_active = False
    query.is_admin = False
    
    db.add(query)
    db.commit()
    db.refresh(query)
    
    return query


def list(search: str, db: Session):
    if(search == None):
        return db.query(Users).options(joinedload(Users.address)).all()
    
    return db.query(Users).options(joinedload(Users.address)).filter(Users.first_name.contains(search)).all()


def get(id: int, db: Session):
    user_exists = db.get(Users, id)
    
    if(not user_exists):
        raise HTTPException(
            detail=f"There is no user with ID {id}",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return user_exists


def delete(id: int, db: Session):
    user = get(id=id, db=db)
    db.delete(user)
    db.commit()
    
    return user


def update(id: int, user: UpdateUserSchema, db: Session):
    instance = get(id=id, db=db)
    exclude_user = user.dict(exclude_unset=True)
    
    if(exclude_user.items()):
        for field in exclude_user:
            setattr(instance, field, exclude_user.get(field))
        
        db.add(instance)
        db.commit()
        db.refresh(instance)
    
    return instance
