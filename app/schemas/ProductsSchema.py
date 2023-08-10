from typing import List
from pydantic import BaseModel, constr, conint
from app.utils.types import ID_TYPE


class BaseAttributeSchema(BaseModel):
    value: constr(min_length=2, max_length=50)


class DisplayAttributeSchema(BaseAttributeSchema):
    id: int


class BaseSkusSchema(BaseModel):
    price: conint(ge=1)
    quantity: conint(ge=1)
    product_id: ID_TYPE


class DisplaySkusSchema(BaseSkusSchema):
    id: int
    attributes: List[DisplayAttributeSchema]


class BaseCategorySchema(BaseModel):
    name: constr(min_length=2, max_length=50)


class DisplayCategorySchema(BaseCategorySchema):
    id: int


class BaseProductSchema(BaseModel):
    name: constr(min_length=2, max_length=50)
    category_id: ID_TYPE


class DisplayProductSchema(BaseModel):
    id: int
    name: str
    category: DisplayCategorySchema
    skus: List[DisplaySkusSchema]


class BaseProductAttributeSchema(BaseModel):
    skus_id: ID_TYPE
    attribute_id: ID_TYPE
