from typing import Annotated, List, Union
from pydantic import BaseModel, Field, constr, conint

class BaseAttributeSchema(BaseModel):
    value: constr(min_length=2, max_length=50)


class DisplayAttributeSchema(BaseAttributeSchema):
    id: int


class BaseSkusSchema(BaseModel):
    price: conint(ge=1)
    quantity: conint(ge=1)
    product_id: conint(ge=1)
    image: str

class UpdateSkusSchema(BaseSkusSchema):
    image: Union[None, str]


class DisplaySkusSchema(BaseSkusSchema):
    id: int
    attributes: List[DisplayAttributeSchema]


class BaseCategorySchema(BaseModel):
    name: constr(min_length=2, max_length=50)


class DisplayCategorySchema(BaseCategorySchema):
    id: int


class BaseProductSchema(BaseModel):
    name: constr(min_length=2, max_length=50)
    category_id: conint(ge=1)


class UpdateProductSchema(BaseProductSchema):
    __annotations__ = { K: Annotated[V, Field(default=None)] for K, V in BaseProductSchema.__annotations__.items() }


class DisplayProductSchema(BaseModel):
    id: int
    name: str
    category: DisplayCategorySchema
    skus: List[DisplaySkusSchema]


class BaseProductAttributeSchema(BaseModel):
    skus_id: conint(ge=1)
    attribute_id: conint(ge=1)
