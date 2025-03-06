# from ...utils import create_order

# import pytest
# from typing import Annotated, TypeVar, get_args
# from api.schemas.models import User
# from fastapi import params
# from httpx import AsyncClient
# from typing import Callable, Awaitable
# from bson import ObjectID

# T = TypeVar("T")

# GetAuthenticatedAsyncClient = Callable[[User], Awaitable[AsyncClient]]


# def get_fastapi_dependency_from_annotation(a: Annotated[T, params.Depends]) -> T:
#     return get_args(a)[1].dependency


# @pytest.fixture()
# def app():
#     from api.main import app

#     yield app


# @pytest.fixture()
# def get_authenticated_async_client(
#     app,
# ):
#     async def _authenticated_client(user: User) -> AsyncClient:

#         # Override the dependency to act as if a user is authenticated
#         dep = get_fastapi_dependency_from_annotation(user)
#         app.dependency_overrides[dep] = lambda: user

#         return AsyncClient(app=app, base_url="http://test")

#     yield _authenticated_client

#     app.dependency_overrides = {}


# @pytest.mark.asyncio
# async def test_get_cart_with_existing_order(test_client, test_session):
#     # new_order = await create_new_order
#     # # print(new_order)
#     # # order_created = await create_new_order(test_session, new_order)
#     # # print(order_created)

#     # expected_id = str(new_order["_id"])

#     user_data = {
#         "id": ObjectID(),
#         "is_active": True,
#         "is_superuser": False,
#         "hashed_password": "test",
#         "email": "test@user.com",
#     }
#     user = User(**user_data)

#     client = await get_authenticated_async_client(user)

#     response = await client.get("/cart")
#     print(response.json())
#     assert response.status_code == 200
#     assert len(response.json()) > 0
# assert response.json()["_id"] == expected_id


# def test_get_cart_with_empty_order(test_client):
#     # # Arrange
#     # user_id = 1
#     # mock_repo.get_order.return_value = None

#     # Act
#     response = test_client.get("/cart")

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Cart is empty"}
