from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    is_active: bool
    is_superuser: bool
