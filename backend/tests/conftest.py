import fastapi_users.fastapi_users
import pytest
from unittest.mock import patch
from beanie import init_beanie
from src.api.schemas.models import User
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
import asyncio
import fastapi_users

import pytest
from src.modules.products.infrastructure.product_repository import (
    MongoDBProductRepository,
)
from fastapi import params
from typing import Annotated, TypeVar, get_args, Generator
from src.api.schemas.models import User
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from typing import Callable, Awaitable
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from src.api.settings import settings
from api.dependencies.auth import current_superuser, get_current_superuser
from src.api.main import app

T = TypeVar("T")

AuthenticatedUser = Annotated[User, Depends(current_superuser)]
GetAuthenticatedAsyncClient = Callable[[User], Awaitable[AsyncClient]]
from api.infrastructure.client import mongodb_instance


# @pytest.fixture(scope="session")
# def app() -> Generator[FastAPI, None, None]:
#     from src.api.main import app

#     yield app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def mongodb(event_loop):
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


# @pytest_asyncio.fixture(scope="function")
# def client_auth_admin(app):
#     async def _authenticated_client(user: User) -> AsyncClient:
#         dep = get_fastapi_dependency_from_annotation(AuthenticatedUser)
#         app.dependency_overrides[dep] = lambda: user

#         return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

#     yield _authenticated_client

#     app.dependency_overrides = {}


# @pytest.fixture()
# def client_auth_admin(app):
#     async def _authenticated_client(user: User) -> AsyncClient:
#         # Override the dependency to act as if a user is authenticated
#         dep = get_fastapi_dependency_from_annotation(AuthenticatedUser)
#         app.dependency_overrides[dep] = lambda: user

#         return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

#     yield _authenticated_client

#     # Remove override
#     app.dependency_overrides = {}


# @pytest_asyncio.fixture(scope="function")
# async def product_created(mongodb, product):
#     product_doc = await mongodb["users"].insert_one(product)
#     return product_doc.inserted_id
