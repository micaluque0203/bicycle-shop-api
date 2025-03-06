from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr
from pymongo.collation import Collation

from modules.iam.domain.entities import User


class UserRead(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    is_active: bool
    is_superuser: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_superuser: Optional[bool] = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]


class UserDB(User):
    hashed_password: str
