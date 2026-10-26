from jsonschema import validate
from tests.config import BASE_URL
from schemas.cart_schema import CART_CREATE_SCHEMA


def test_create_cart_success(api_client):
    payload = {
        "userId": 1,
        "products": [
            {"productId": 1, "quantity": 2},
            {"productId": 2, "quantity": 1}
        ]
    }

    response = api_client.post(f"{BASE_URL}/carts", json=payload)

    assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}. Тело: {response.text}"

    created = response.json()
    assert "id" in created, f"В ответе нет id: {created}"
    assert created["userId"] == payload["userId"]
    assert len(created["products"]) == len(payload["products"])

    validate(instance=created, schema=CART_CREATE_SCHEMA)


def test_update_cart_success(api_client):
    payload = {
        "userId": 1,
        "products": [
            {"productId": 3, "quantity": 5}
        ]
    }

    response = api_client.put(f"{BASE_URL}/carts/1", json=payload)

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

    updated = response.json()
    assert updated["userId"] == payload["userId"]
    assert len(updated["products"]) == 1
    assert updated["products"][0]["productId"] == 3


def test_delete_cart_success(api_client):
    response = api_client.delete(f"{BASE_URL}/carts/1")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

    deleted = response.json()
    assert deleted["id"] == 1
    assert "userId" in deleted
