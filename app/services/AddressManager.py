from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.AddressSchema import BaseAddressSchema, IranProvinces, UpdateAddressSchema
from app.schemas.UsersSchema import AuthUserSchema
from app.models.AddressModel import Address
from app.utils.exceptions import not_found_exception, unuthorized


def create(address: BaseAddressSchema, current_user: AuthUserSchema, db: Session):
    query = Address()
    
    query.address = address.address
    query.city = address.city
    query.postcode = address.postcode
    query.province = address.province.value
    query.user_id = current_user.id
    
    db.add(query)
    db.commit()
    db.refresh(query)
    
    return query


def get(current_user: AuthUserSchema, db: Session):
    instance = db.query(Address).filter(Address.user_id == current_user.id).all()
    if instance:
        return instance
    
    not_found_exception("آدرسی")


def delete(id: int, current_user: AuthUserSchema, db: Session):
    instance = db.get(Address, id)
    
    if(instance):
        if(instance.user_id == current_user.id):
            db.delete(instance)
            db.commit()
            
            return instance
        unuthorized()
    not_found_exception("آدرسی")


def update(address: UpdateAddressSchema, id: int, current_user: AuthUserSchema, db: Session):
    instance = db.get(Address, id)
    if(instance):
        if(instance.user_id == current_user.id):
            exclude_address = address.dict(exclude_unset=True)
            
            if(exclude_address.items()):
                for field in exclude_address:
                    if(type(exclude_address.get(field)) == IranProvinces):
                        setattr(instance, field, exclude_address.get(field).value)
                    else:
                        setattr(instance, field, exclude_address.get(field))

                db.add(instance)
                db.commit()
                db.refresh(instance)
            return instance
        unuthorized()
    not_found_exception("آدرسی")
