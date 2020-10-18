from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from ..db.mongodb import AsyncIOMotorClient
from ..models.movie import MovieInDB