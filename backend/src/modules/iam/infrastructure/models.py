from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field
from pymongo.collation import Collation

from modules.iam.domain.entities import User


class UserRead(schemas.BaseUser[int]):
    id: PydanticObjectId
    email: EmailStr = Field(None, alias="username")
    is_active: bool
    is_superuser: bool


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_superuser: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]


class UserDB(User):
    hashed_password: str
