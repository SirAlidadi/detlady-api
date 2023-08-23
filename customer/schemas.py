import re
from typing import Annotated, List
from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from address.schemas import BaseAddressSchema

class BaseUserSchema(BaseModel):
    first_name: constr(min_length=2, max_length=50)
    last_name: constr(min_length=2, max_length=50)
    phone: constr(min_length=10, max_length=11)
    
    @field_validator('phone')
    def phone_validator(cls, field):
        digits_only = re.sub(r'\D', '', field)
        pattern = r'^0?9\d{9}$'
        
        if(not re.match(pattern, digits_only)):
            raise ValueError(f'The ${field} is not valid.')
        
        return digits_only
    
    
    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(BaseUserSchema):
    password: constr(min_length=8, max_length=16)


class DisplayUserSchema(BaseUserSchema):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    address: List[BaseAddressSchema] = Field(alias="addresses")


class UpdateUserSchema(BaseUserSchema):
    __annotations__ = { K: Annotated[V, Field(default=None)] for K, V in BaseUserSchema.__annotations__.items() }


class AuthUserSchema(BaseUserSchema):
    is_active: bool
    is_admin: bool


class DeleteUsersSchema(BaseModel):
    ids: List[int]