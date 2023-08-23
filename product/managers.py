from .models import Attributes, ProductAttributes, ProductCategories, ProductSkus, Products
from .schemas import BaseProductAttributeSchema
from sqlalchemy.orm import Session
from core.model_manager import BaseModelManager


class CategoryManager(BaseModelManager):
    def __init__(self, model):
        super().__init__(model)

category_manager = CategoryManager(ProductCategories)


class ProductManager(BaseModelManager):
    def __init__(self, model):
        super().__init__(model)

    def create(self, data: dict, db: Session):
        category_manager.get(data.get('category_id'), db)
        return super().create(data, db)

product_manager = ProductManager(Products)


class AttributeManager(BaseModelManager):
    def __init__(self, model):
        super().__init__(model)


attribute_manager = AttributeManager(Attributes)


class SkusManager(BaseModelManager):
    def __init__(self, model):
        super().__init__(model)
    
    def update(self, data: dict, id: int, db: Session):
        product_manager.get(data.get("product_id"), db=db)
        return super().update(data, id, db)


skus_manager = SkusManager(ProductSkus)


class ProductAttributeManager(BaseModelManager):
    def __init__(self, model):
        super().__init__(model)
    
    def create(self, data: dict, db: Session):
        skus_manager.get(id=data.get("skus_id"), db=db)
        attribute_manager.get(id=data.get("attribute_id"), db=db)
        return super().create(data, db)


product_attribute_manager = ProductAttributeManager(ProductAttributes)