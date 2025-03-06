import pytest
import json

from src.api.schemas.models import UserCreate
from api.dependencies.auth import get_user_manager


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


@pytest.mark.asyncio
async def test_get_products(mongodb, product, client_no_auth):
    product_created = await mongodb["products"].insert_one(product)

    response = await client_no_auth.get("/products")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["_id"] == str(product_created.inserted_id)


@pytest.mark.asyncio
async def test_get_product_by_id(mongodb, client_no_auth, product):
    product_created = await mongodb["products"].insert_one(product)
    expected_id = str(product_created.inserted_id)
    response = await client_no_auth.get(f"/products/{expected_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()["_id"] == expected_id


@pytest.mark.asyncio
async def test_no_admin_cannot_create_product(client_no_auth, product):
    response = await client_no_auth.post(
        "/admin/products",
        data=json.dumps(product),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.asyncio
async def test_admin_can_create_product(
    client_no_auth, superuser_token_headers, product
):
    headers = {**superuser_token_headers, "Content-Type": "application/json"}

    response = await client_no_auth.post(
        "/admin/products", data=json.dumps(product), headers=headers
    )
    print(response.json())
    assert response.status_code == 201
    assert "_id" in response.json()


@pytest.mark.asyncio
async def test_admin_can_delete_product(
    client_no_auth, superuser_token_headers, product, mongodb
):
    new_product = await mongodb["products"].insert_one(product)
    expected_id = str(new_product.inserted_id)
    url = f"/admin/products/{expected_id}"
    response = await client_no_auth.delete(url, headers=superuser_token_headers)
    assert response.status_code == 204
