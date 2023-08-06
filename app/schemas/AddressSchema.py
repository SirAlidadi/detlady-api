from enum import Enum
from typing import Annotated
import re
from pydantic import BaseModel, ConfigDict, constr, conint, field_validator, Field


class IranProvinces(Enum):
    ALBORZ = "البرز"
    ARDABIL = "اردبیل"
    AZERBAIJAN_EAST = "آذربایجان شرقی"
    AZERBAIJAN_WEST = "آذربایجان غربی"
    BUSHEHR = "بوشهر"
    CHAHARMAHAL_BAKHTIARI = "چهارمحال و بختیاری"
    FARS = "فارس"
    GILAN = "گیلان"
    GOLESTAN = "گلستان"
    HAMEDAN = "همدان"
    HORMOZGAN = "هرمزگان"
    ILAM = "ایلام"
    ISFAHAN = "اصفهان"
    KERMAN = "کرمان"
    KERMANSHAH = "کرمانشاه"
    KHORASAN_NORTH = "خراسان شمالی"
    KHORASAN_RAZAVI = "خراسان رضوی"
    KHORASAN_SOUTH = "خراسان جنوبی"
    KHUZESTAN = "خوزستان"
    KOHGILUYEH_BOYER_AHMAD = "کهگیلویه و بویراحمد"
    KURDISTAN = "کردستان"
    LORESTAN = "لرستان"
    MARKAZI = "مرکزی"
    MAZANDARAN = "مازندران"
    QAZVIN = "قزوین"
    QOM = "قم"
    SEMNAN = "سمنان"
    SISTAN_BALUCHESTAN = "سیستان و بلوچستان"
    TEHRAN = "تهران"
    YAZD = "یزد"
    ZANJAN = "زنجان"


class BaseAddressSchema(BaseModel):
    province: IranProvinces
    city: constr(min_length=2, max_length=50)
    address: constr(min_length=2, max_length=255)
    postcode: constr(min_length=10, max_length=10)
    
    @field_validator('postcode')
    def postcode_validator(cls, field):
        digits_only = re.sub(r'\D', '', field)
        pattern = r'\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b'
        
        if(not re.match(pattern, digits_only)):
            raise ValueError(f'The ${field} is not valid.')
        
        return digits_only
    
    
    model_config = ConfigDict(from_attributes=True)


class UpdateAddressSchema(BaseAddressSchema):
    __annotations__ = { K: Annotated[V, Field(default=None)] for K, V in BaseAddressSchema.__annotations__.items() }
