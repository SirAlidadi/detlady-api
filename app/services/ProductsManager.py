from app.models.ProductsModel import Attributes, ProductCategories, ProductSkus, Products, product_attribute
from app.schemas.ProductsSchema import BaseAttributeSchema, BaseCategorySchema, BaseProductAttributeSchema, BaseProductSchema, BaseSkusSchema
from sqlalchemy.orm import Session
from app.utils.exceptions import not_found_exception


def create_category(category: BaseCategorySchema, db: Session):
    product_category = ProductCategories()
    product_category.name = category.name
    
    db.add(product_category)
    db.commit()
    db.refresh(product_category)
    
    return product_category


def list_product(db: Session):
    return db.query(Products).all()


def create_product(product: BaseProductSchema, db: Session):
    exists = db.get(ProductCategories, product.category_id)
    
    if (not exists):
        not_found_exception("دسته بندی ای")
        
    instance = Products()
    instance.name = product.name
    instance.category_id = product.category_id
    
    db.add(instance)
    db.commit()
    db.refresh(instance)
    
    return instance


def get_product(id: int, db: Session):
    instance = db.get(Products, id)
    
    if (not instance):
        not_found_exception("محصولی")
        
    return instance


def create_attribute(attribute: BaseAttributeSchema, db: Session):
    instance = Attributes()
    instance.value = attribute.value
    
    db.add(instance=instance)
    db.commit()
    db.refresh(instance)
    
    return instance


def list_attribute(db: Session):
    return db.query(Attributes).all()


def create_skus(skus: BaseSkusSchema, db: Session):
    instance = ProductSkus()
    
    instance.image = "https://google.com"
    instance.price = skus.price
    instance.quantity = skus.quantity
    instance.product_id = skus.product_id
    
    db.add(instance)
    db.commit()
    db.refresh(instance)
    
    return instance


def create_relation_product_attribute(relation: BaseProductAttributeSchema, db: Session):
    instance = product_attribute.insert().values(product_skus_id=relation.skus_id, attribute_id=relation.attribute_id)
    db.execute(instance)
    
    return relation
    