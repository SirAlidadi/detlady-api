from fastapi import HTTPException, status


def unuthorized(message: str = "شما دسترسی به این بخش ندارید."):
    raise HTTPException(detail=message, status_code=status.HTTP_401_UNAUTHORIZED)


def not_found_exception(field_name: str = "فیلدی"):
    raise HTTPException(detail=f"{field_name} در دیتابیس با این مشخصات وجود ندارد", status_code=status.HTTP_401_UNAUTHORIZED)
