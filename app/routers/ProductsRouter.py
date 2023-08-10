from typing import List
from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.schemas.ProductsSchema import BaseAttributeSchema, BaseCategorySchema, BaseProductAttributeSchema, BaseSkusSchema, DisplayAttributeSchema, DisplayCategorySchema, DisplayProductSchema, BaseProductSchema
from sqlalchemy.orm import Session
from app.utils.types import ID_TYPE
from app.services.ProductsManager import create_category as orm_create_category,\
                                         create_product as orm_create_product,\
                                         list_product as orm_list_product,\
                                         create_attribute as orm_create_attribute,\
                                         list_attribute as orm_list_attribute,\
                                         create_skus as orm_create_skus,\
                                         create_relation_product_attribute,\
                                         get_product as orm_get_product


router = APIRouter(prefix="/product", tags=["Products"])

@router.get('/', response_model=List[DisplayProductSchema])
def list_product(db: Session = Depends(get_db)):
    return orm_list_product(db)


@router.post('/create', response_model=DisplayProductSchema)
def create_product(request: BaseProductSchema, db: Session = Depends(get_db)):
    return orm_create_product(request, db)


@router.get('/{product_id}', response_model=DisplayProductSchema)
def get_product(product_id: ID_TYPE, db: Session = Depends(get_db)):
    return orm_get_product(product_id, db)


@router.post('/categories/create', response_model=DisplayCategorySchema)
def create_category(request: BaseCategorySchema, db: Session = Depends(get_db)):
    return orm_create_category(request, db)


@router.post('/attributes/create', response_model=DisplayAttributeSchema)
def create_attribute(request: BaseAttributeSchema, db: Session = Depends(get_db)):
    return orm_create_attribute(request, db)


@router.get('/attributes', response_model=List[DisplayAttributeSchema])
def list_attribute(db: Session = Depends(get_db)):
    return orm_list_attribute(db)


@router.post('/skus/create')
def create_skus(skus: BaseSkusSchema, db: Session = Depends(get_db)):
    return orm_create_skus(skus, db)


@router.post('/skus/add')
def create_skus_realation(relation: BaseProductAttributeSchema, db: Session = Depends(get_db)):
    return create_relation_product_attribute(relation, db)
