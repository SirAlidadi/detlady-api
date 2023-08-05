
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.UsersModel import Users
from app.schemas.UsersSchema import CreateUserSchema, UpdateUserSchema


def create(user: CreateUserSchema, db: Session):
    user_exists = db.query(Users).filter(Users.phone == user.phone).first()
    if(user_exists):
        raise HTTPException(
            detail="There is a user with this phone number",
            status_code=status.HTTP_409_CONFLICT
        ) 
        
    query = Users()
    for field in user:
        setattr(query, field[0], field[1])

    query.is_active = False
    query.is_admin = False
    
    db.add(query)
    db.commit()
    db.refresh(query)
    
    return query


def list(search: str, db: Session):
    if(search == None):
        return db.query(Users).all()
    
    return db.query(Users).filter(Users.first_name.contains(search)).all()

def get(id: int, db: Session):
    user = db.get(Users, id)
    
    if(not user):
        raise HTTPException(
            detail=f"There is no user with ID {id}",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return user


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
