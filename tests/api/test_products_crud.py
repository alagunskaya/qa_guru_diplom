from tests.config import BASE_URL
from schemas.product_schema import PRODUCT_CREATE_SCHEMA
from jsonschema import validate


def test_create_product_success(api_client):
    payload = {
        "title": "Test Product",
        "price": 42.5,
        "description": "API tests",
        "image": "https://i.pravatar.cc",
        "category": "electronics"
    }

    response = api_client.post(f"{BASE_URL}/products", json=payload)

    assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}. Тело: {response.text}"

    created = response.json()
    assert "id" in created, f"В ответе нет id: {created}"
    assert created["title"] == payload["title"]
    assert created["price"] == payload["price"]
    validate(instance=created, schema=PRODUCT_CREATE_SCHEMA)


def test_update_product_success(api_client):
    payload = {
        "title": "Updated Title",
        "price": 99.99,
        "description": "Updated description",
        "image": "https://i.pravatar.cc",
        "category": "electronics"
    }

    response = api_client.put(f"{BASE_URL}/products/1", json=payload)

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

    updated = response.json()
    assert updated["title"] == payload["title"]
    assert updated["price"] == payload["price"]


def test_delete_product_success(api_client):
    response = api_client.delete(f"{BASE_URL}/products/1")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

    deleted = response.json()
    assert deleted["id"] == 1
    assert "title" in deleted
