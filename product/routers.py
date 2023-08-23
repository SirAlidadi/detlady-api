from typing import Annotated, List, Optional
from fastapi import APIRouter, Body, Depends, File, Path, Request, Response, UploadFile, status
from pydantic import ValidationError
from core.database import get_db
from .schemas import BaseAttributeSchema, BaseCategorySchema, BaseProductAttributeSchema, BaseSkusSchema, DisplayAttributeSchema, DisplayCategorySchema, DisplayProductSchema, BaseProductSchema, UpdateProductSchema, UpdateSkusSchema
from sqlalchemy.orm import Session
from .managers import product_manager, category_manager, attribute_manager, skus_manager, product_attribute_manager
from core.upload_file import upload_image


router = APIRouter(prefix="/product", tags=["Products"])


@router.get('/', response_model=List[DisplayProductSchema])
def list_product(db: Session = Depends(get_db)):
    return product_manager.get_all(db=db)


@router.post('/create', response_model=DisplayProductSchema)
def create_product(request: BaseProductSchema, db: Session = Depends(get_db)):
    return product_manager.create(data=request.model_dump(), db=db)


@router.get('/{product_id}', response_model=DisplayProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_manager.get(db=db, id=product_id)


@router.delete('/delete/{product_id}',)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_manager.delete(id=product_id, db=db)


@router.patch('/update/{product_id}')
def update_product(product_id: int, request: UpdateProductSchema, db: Session = Depends(get_db)):
    return product_manager.update(
        data=request.model_dump(exclude_unset=True),
        id=product_id,
        db=db
    )


@router.get('/category/', response_model=List[DisplayCategorySchema])
def list_category(db: Session = Depends(get_db)):
    return category_manager.get_all(db=db)


@router.post('/category/create', response_model=DisplayCategorySchema)
def create_category(request: BaseCategorySchema, db: Session = Depends(get_db)):
    return category_manager.create(
        data=request.model_dump(),
        db=db
    )


@router.get('/category/{category_id}', response_model=DisplayCategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_manager.get(
        id=category_id,
        db=db
    )


@router.delete('/category/delete/{category_id}', response_model=DisplayCategorySchema)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_manager.delete(id=category_id, db=db)


@router.patch('/category/update/{category_id}', response_model=DisplayCategorySchema)
def update_category(request: BaseCategorySchema, category_id: int, db: Session = Depends(get_db)):
    return category_manager.update(data=request.model_dump(), id=category_id, db=db)


@router.get('/attribute/', response_model=List[DisplayAttributeSchema])
def list_attribute(db: Session = Depends(get_db)):
    return attribute_manager.get_all(db=db)


@router.post('/attribute/create', response_model=DisplayAttributeSchema)
def create_attribute(request: BaseAttributeSchema, db: Session = Depends(get_db)):
    return attribute_manager.create(data=request.model_dump(), db=db)


@router.get('/attribute/{attribute_id}', response_model=DisplayAttributeSchema)
def get_attribute(attribute_id: int, db: Session = Depends(get_db)):
    return attribute_manager.get(id=attribute_id, db=db)


@router.delete('/attribute/delete/{attribute_id}', response_model=DisplayAttributeSchema)
def delete_attribute(attribute_id: int, db: Session = Depends(get_db)):
    return attribute_manager.delete(db=db, id=attribute_id)


@router.patch('/attribute/update/{attribute_id}', response_model=DisplayAttributeSchema)
def delete_attribute(attribute_id: int, request: BaseAttributeSchema, db: Session = Depends(get_db)):
    return attribute_manager.update(data=request.model_dump(), id=attribute_id, db=db)


@router.post('/skus/create')
async def create_skus(
    response: Response,
    request: Request,
    price: Annotated[int, Body()],
    product_id: Annotated[int, Body()],
    quantity: Annotated[int, Body()],
    image: Annotated[UploadFile, File()],
    db: Session = Depends(get_db)
):
    try:
        form_data = BaseSkusSchema(
            price=price,
            product_id=product_id,
            quantity=quantity,
            image=f"{request.base_url}media/{upload_image(image=image, dir='media/')}"
        )
    except ValidationError as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return e.errors()
    
    return skus_manager.create(
        data=form_data.model_dump(),
        db=db
    )


@router.patch('/skus/update/{skus_id}')
async def update_skus(
    response: Response,
    request: Request,
    skus_id: Annotated[int, Path()],
    price: Annotated[int, Body()],
    product_id: Annotated[int, Body()],
    quantity: Annotated[int, Body()],
    image: UploadFile = Optional[File()],
    db: Session = Depends(get_db)
):

    try:
        form_data = UpdateSkusSchema(
            price=price,
            product_id=product_id,
            quantity=quantity,
            image=None if not hasattr(image, "filename") else f"{request.base_url}media/{upload_image(image=image, dir='media/')}"
        )
    except ValidationError as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return e.errors()

    return skus_manager.update(
        id=skus_id,
        data=form_data.model_dump(exclude_none=True),
        db=db
    )


@router.delete('/skus/delete/{skus_id}')
async def delete_skus(skus_id: int, db = Depends(get_db)):
    return skus_manager.delete(skus_id, db=db)


@router.post('/skus/relation/create')
def create_skus_realation(request: BaseProductAttributeSchema, db: Session = Depends(get_db)):
    return product_attribute_manager.create(
        request.model_dump(),
        db=db
    )


@router.delete('/skus/relation/delete/{relation_id}')
def create_skus_realation(relation_id: int, db: Session = Depends(get_db)):
    return product_attribute_manager.delete(id=relation_id, db=db)