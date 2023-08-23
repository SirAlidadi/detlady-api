from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.model_manager import BaseModelManager
from .models import Address


class AddressManager(BaseModelManager):
    def __init__(self, model):
        super().__init__(model)
    
    def create(self, data: dict, user_id: int, db: Session):
        query = Address()
    
        query.address = data.get("address")
        query.city = data.get("city")
        query.postcode = data.get("postcode")
        query.province = data.get("province").value
        query.user_id = user_id
        
        db.add(query)
        db.commit()
        db.refresh(query)
        
        return query
    
    def get_all(self, user_id: int, db: Session):
        return db.query(Address).filter(Address.user_id == user_id).all()
    
    def delete(self, id: int, user_id: int, db: Session):
        instance = self.get(id=id, db=db)
        
        if(instance.user_id == user_id):
            return super().delete(id, db)
        
        raise HTTPException(
            detail=f"شما مجاز به ادامه این عملیات نمی باشید.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    def update(self, data: dict, id: int, user_id: int, db: Session):
        instance = self.get(id=id, db=db)
        
        if(user_id == instance.user_id):
            return super().update(data, id, db)

        raise HTTPException(
            detail=f"شما مجاز به ادامه این عملیات نمی باشید.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

address_manager = AddressManager(Address)
