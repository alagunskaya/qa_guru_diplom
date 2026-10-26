import pytest
from jsonschema import validate
from tests.config import BASE_URL
from schemas.cart_schema import CARTS_LIST_SCHEMA, CART_SCHEMA


def test_get_all_carts_matches_schema(api_client):
    response = api_client.get(f"{BASE_URL}/carts")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    validate(instance=response.json(), schema=CARTS_LIST_SCHEMA)


def test_get_single_cart_matches_schema(api_client):
    response = api_client.get(f"{BASE_URL}/carts/1")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    cart = response.json()
    validate(instance=cart, schema=CART_SCHEMA)
    assert cart["id"] == 1


@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 8])
def test_get_carts_by_user(api_client, user_id):
    response = api_client.get(f"{BASE_URL}/carts/user/{user_id}")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    carts = response.json()
    assert len(carts) > 0, f"У пользователя {user_id} нет корзин"

    for cart in carts:
        assert cart["userId"] == user_id, f"Корзина {cart['id']} принадлежит {cart['userId']}, а не {user_id}"


def test_get_carts_for_nonexistent_user(api_client):
    response = api_client.get(f"{BASE_URL}/carts/user/999")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
    carts = response.json()
    assert carts == [], f"Ожидали пустой список, получили {carts}"


def test_cart_products_reference_existing_products(api_client):
    products_response = api_client.get(f"{BASE_URL}/products")
    existing_ids = {p["id"] for p in products_response.json()}

    carts_response = api_client.get(f"{BASE_URL}/carts")
    carts = carts_response.json()

    for cart in carts:
        for item in cart["products"]:
            assert item["productId"] in existing_ids, f"В корзине {cart['id']} несуществующий товар {item['productId']}"


def test_cart_quantities_are_positive(api_client):
    response = api_client.get(f"{BASE_URL}/carts")
    carts = response.json()

    for cart in carts:
        for item in cart["products"]:
            assert item["quantity"] > 0, f"Корзина {cart['id']}, товар {item['productId']}: quantity={item['quantity']}"
