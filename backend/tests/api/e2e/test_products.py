import json

import pytest
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies.auth import get_user_manager
from src.modules.iam.infrastructure.models import UserCreate

# @pytest.fixture(scope="module")
# async def superuser_token_headers(client_no_auth, event_loop):

#     response = await client_no_auth.post(
#         "/auth/jwt/login",
#         data={"username": "admin@example.com", "password": "password123"},
#     )
#     tokens = response.json()
#     headers = {"Authorization": f"Bearer {tokens['access_token']}"}
#     return headers


@pytest.fixture(scope="module")
async def superuser_token_headers(client_no_auth):
    async for user_manager in get_user_manager():
        superuser = UserCreate(
            email="admin@example.com",
            password="password123",
            is_superuser=True,
        )
        await user_manager.create(superuser)
        response = await client_no_auth.post(
            "/auth/jwt/login",
            data={"username": "admin@example.com", "password": "password123"},
        )
        tokens = response.json()
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        return headers


class TestProducts:
    @pytest.mark.asyncio
    async def test_get_products(self, mongodb, product, client_no_auth):
        product_created = await mongodb["products"].insert_one(product)
        print(product_created)
        response = await client_no_auth.get("/products")
        print(response.json())
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[0]["product_id"] == str(product_created.inserted_id)

    @pytest.mark.asyncio
    async def test_get_product_by_id(self, mongodb, client_no_auth, product):
        product_created = await mongodb["products"].insert_one(product)
        expected_id = str(product_created.inserted_id)
        response = await client_no_auth.get(f"/products/{expected_id}")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()["product_id"] == expected_id

    @pytest.mark.asyncio
    async def test_no_admin_cannot_create_product(self, client_no_auth, product):
        response = await client_no_auth.post(
            "/admin/products",
            data=json.dumps(product),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}

    # @pytest.mark.asyncio
    # async def test_admin_can_create_product(self, client_no_auth, product, mongodb):
    #     # async for user_manager in get_user_manager():
    #     superuser = UserCreate(
    #         email="admin@example.com",
    #         password="password123",
    #         is_superuser=True,
    #     )
    #     # await user_manager.create(superuser)

    #     await mongodb["users"].insert_one(superuser.model_dump())

    #     async for user_manager in get_user_manager():
    #         credentials = OAuth2PasswordRequestForm(
    #             username=superuser.email, password=superuser.password
    #         )
    #         tokens = await user_manager.authenticate(credentials)
    #         print(tokens)

    #     superuser_token_headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    #     headers = {**superuser_token_headers, "Content-Type": "application/json"}

    #     response = await client_no_auth.post(
    #         "/admin/products", data=json.dumps(product), headers=headers
    #     )
    #     print(response.json())
    #     assert response.status_code == 201
    #     assert "_id" in response.json()

    # @pytest.mark.asyncio
    # async def test_admin_can_delete_product(
    #     self, client_no_auth, superuser_token_headers, product, mongodb
    # ):
    #     new_product = await mongodb["products"].insert_one(product)
    #     expected_id = str(new_product.inserted_id)
    #     url = f"/admin/products/{expected_id}"
    #     response = await client_no_auth.delete(url, headers=superuser_token_headers)
    #     assert response.status_code == 204
