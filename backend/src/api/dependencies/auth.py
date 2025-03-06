from typing import Any, Coroutine, Optional

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_beanie import BeanieUserDatabase

from api.infrastructure.client import get_mongodb
from api.security import get_password_hash, verify_password
from api.settings import settings
from modules.iam.domain.entities import User


async def get_user_db():
    async for db in get_mongodb():
        yield BeanieUserDatabase(User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret, lifetime_seconds=settings.jwt_token_lifetime
    )


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])


def get_current_user():
    return fastapi_users.current_user(active=True)


def get_current_superuser():
    user = fastapi_users.current_user(active=True, superuser=True)
    return user


current_superuser = get_current_superuser()
current_active_user = get_current_user()
