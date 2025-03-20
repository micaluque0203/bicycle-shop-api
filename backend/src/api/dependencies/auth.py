import contextlib

from beanie import PydanticObjectId
from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_beanie import BeanieUserDatabase

from api.settings import Settings
from modules.iam.domain.entities import User
from modules.iam.infrastructure.user_repository import UserManager

settings = Settings()


@contextlib.asynccontextmanager
async def get_user_db():
    yield BeanieUserDatabase(User)


async def get_user_manager():
    async with get_user_db() as user_db:
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
    return fastapi_users.current_user(active=True)


current_superuser = get_current_superuser()
current_active_user = get_current_user()
