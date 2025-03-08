from typing import Optional

from bson import ObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager
from passlib.context import CryptContext

from api.infrastructure.client import get_mongodb
from modules.iam.domain.entities import User
from modules.iam.infrastructure.models import UserCreate, UserDB, UserRead

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB

    def on_after_register(self, user: UserDB, request: Request):
        print(f"User {user.inserted_id} has registered.")

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> UserDB:
        await self.validate_password(user_create.password, user_create)
        existing_user = await self.get_by_email(user_create.email)
        if existing_user:
            raise Exception  # TODO: Create custom exception
        user_dict = user_create.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        if safe:
            user_dict.pop("is_superuser", None)
            user_dict.pop("is_verified", None)
        user = self.user_db_model(**user_dict)

        if user_create.is_superuser:
            user.is_superuser = True

        created = await self.create_user(user_create)
        self.on_after_register(created, request)
        return user

    async def create_user(self, user_create: UserCreate):
        async for db in get_mongodb():
            user = user_create.model_dump()
            user_doc = await db.users.insert_one(user)
            if user_doc:
                return user_doc

    async def get_by_email(self, user_email: str) -> UserCreate:
        async for db in get_mongodb():
            user_doc = await db.users.find_one({"email": user_email})
            if user_doc:
                return self.user_db_model(**user_doc)

    async def authenticate(self, credentials):
        user = await self.get_by_email(credentials.username)
        if user is None or not verify_password(
            credentials.password, user.hashed_password
        ):
            return None
        return user

    async def get(self, user_id: str) -> User:
        async for db in get_mongodb():
            user = await db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                return User(**user)

    @staticmethod
    def parse_id(user_id: str) -> ObjectId:
        return ObjectId(user_id)
