from ast import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class BaseModelManager:
    def __init__(self, model):
        self.model = model
    
    
    def get(self, id: int, db: Session) -> Session:
        instance = db.get(self.model, id)

        if not instance:
            raise HTTPException(
                detail=f"اطلاعاتی با این شناسه در دیتابیس موجود نیست",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return instance
    
    def get_all(self, db: Session):
        return db.query(self.model).all()
    
    
    def delete(self, id: int, db: Session):
        instance = self.get(id, db)
        
        db.delete(instance)
        db.commit()
        
        return instance
    
    
    def deleteAll(self, items, db: Session):
        query = db.query(self.model).filter(self.model.id.in_(items.ids))
        instance = query.all()
        query.delete()
        db.commit()
        
        return instance

    
    def update(self, data: dict, id: int, db: Session):
        instance = self.get(id, db)

        for Key in data:
            setattr(instance, Key, data[Key])
        
        db.add(instance)
        db.commit()
        db.refresh(instance)
        
        return instance
    
    
    def create(self, data: dict, db: Session):
        instance = self.model()
        
        for Key in data:
            setattr(instance, Key, data[Key])
        
        db.add(instance)
        db.commit()
        db.refresh(instance)
        
        return instance
