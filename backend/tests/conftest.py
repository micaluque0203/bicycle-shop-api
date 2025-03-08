import asyncio
import os
from typing import Annotated, Awaitable, Callable, TypeVar, get_args
from unittest.mock import patch

import fastapi_users
import fastapi_users.fastapi_users
import pytest
import pytest_asyncio
from beanie import init_beanie
from fastapi import Depends, params
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from api.dependencies.auth import current_superuser, get_current_superuser
from src.api.main import app
from src.api.settings import Settings
from src.modules.iam.domain.entities import User

T = TypeVar("T")

AuthenticatedUser = Annotated[User, Depends(current_superuser)]
GetAuthenticatedAsyncClient = Callable[[User], Awaitable[AsyncClient]]


# @pytest.fixture(scope="session", autouse=True)
# def mock_settings():
#     os.environ["MONGODB_URL"] = "mongodb://admin:password@127.0.0.1:27017"
#     os.environ["DATABASE_NAME"] = "test_db"

#     print(os.getenv("MONGODB_URL"))
#     print(os.getenv("DATABASE_NAME"))


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def settings():
    with patch("src.api.settings.Settings", autospec=True) as mock_settings:
        mock_settings.return_value.mongodb_url = (
            "mongodb://admin:password@127.0.0.1:27017"
        )
        mock_settings.return_value.database_name = "test_db"


@pytest_asyncio.fixture(scope="session")
async def mongodb(event_loop):
    settings = Settings()
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client["test_db"]
    try:
        await init_beanie(database=db, document_models=[User])
        yield db
    finally:
        await db.drop_collection("products")
        client.close()


@pytest_asyncio.fixture(scope="function")
def product():
    return {
        "part_ids": [],
        "configuration_rule_ids": [],
        "name": "test_product",
        "category": "test_category",
    }


@pytest_asyncio.fixture(scope="session")
async def client_no_auth(event_loop):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def client_auth_admin():
    user_data = {
        "is_active": True,
        "is_superuser": True,
        "hashed_password": "test",
        "email": "test@user.com",
    }
    user = User(**user_data)

    app.dependency_overrides[get_current_superuser] = lambda: user

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


def get_fastapi_dependency_from_annotation(a: Annotated[T, params.Depends]) -> T:
    return get_args(a)[1].dependency
