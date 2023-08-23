
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.model_manager import BaseModelManager
from .models import Users
from core.bcrypt import Bcrypt


class UserManager(BaseModelManager):
    def __init__(self, model):
        super().__init__(model)
    
    def create(self, data: dict, db: Session):
        user_exists = db.query(self.model).filter(self.model.phone == data.phone).first()
        if(user_exists):
            raise HTTPException(
                detail="There is a user with this phone number",
                status_code=status.HTTP_409_CONFLICT
            ) 
            
        query = self.model()
        query.first_name = data.first_name
        query.last_name = data.last_name
        query.phone = data.phone
        query.password = Bcrypt.create_bcrypt(data.password)
        query.is_active = False
        query.is_admin = False
        
        db.add(query)
        db.commit()
        db.refresh(query)
        
        return query
    
    def get_all(self, db: Session, search: str):
        if search:
            return db.query(self.model).filter(self.model.first_name.contains(search)).all()
        return super().get_all(db)


user_manager = UserManager(Users)
