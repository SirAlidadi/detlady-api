from typing import Annotated
from fastapi import Path


ID_TYPE = Annotated[int, Path(gt=0)]