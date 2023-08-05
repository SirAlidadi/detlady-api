import re
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, constr, field_validator


class BaseUserSchema(BaseModel):
    first_name: constr(min_length=2, max_length=50)
    last_name: constr(min_length=2, max_length=50)
    phone: constr(min_length=10, max_length=11)
    
    @field_validator('phone')
    def phone_validator(cls, field):
        digits_only = re.sub(r'\D', '', field)
        pattern = r'^0?9\d{9}$'
        
        if(not re.match(pattern, digits_only)):
            raise ValueError('The phone number is not valid.')
        
        return digits_only
    
    
    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(BaseUserSchema):
    password: constr(min_length=8, max_length=16)


class DisplayUserSchema(BaseUserSchema):
    id: int


class UpdateUserSchema(BaseUserSchema):
    __annotations__ = { K: Annotated[V, Field(default=None)] for K, V in BaseUserSchema.__annotations__.items() }
