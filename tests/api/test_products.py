from jsonschema import validate
from tests.config import BASE_URL
from schemas.product_schema import PRODUCTS_LIST_SCHEMA, PRODUCT_SCHEMA


def test_get_all_products_returns_20_items(api_client):
    response = api_client.get(f"{BASE_URL}/products")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    products = response.json()
    assert len(products) == 20, f"Ожидали 20 товаров, получили {len(products)}"


def test_get_all_products_matches_schema(api_client):
    response = api_client.get(f"{BASE_URL}/products")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

    products = response.json()
    validate(instance=products, schema=PRODUCTS_LIST_SCHEMA)


def test_get_single_product_matches_schema(api_client):
    response = api_client.get(f"{BASE_URL}/products/1")

    assert response.status_code == 200

    product = response.json()
    validate(instance=product, schema=PRODUCT_SCHEMA)


def test_get_all_products_unique_ids(api_client):
    response = api_client.get(f"{BASE_URL}/products")
    products = response.json()

    ids = [p["id"] for p in products]
    assert len(ids) == len(set(ids)), f"Найдены дубли ID: {ids}"


def test_get_single_product_success(api_client):
    response = api_client.get(f"{BASE_URL}/products/1")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    product = response.json()
    assert product["id"] == 1
    assert product["title"] == "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"
    assert product["price"] == 109.95
    assert product["category"] == "men's clothing"


def test_get_single_product_not_found(api_client):
    response = api_client.get(f"{BASE_URL}/products/999")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
    assert response.text == "", f"Ожидали пустое тело, получили: {response.text}"


def test_get_categories(api_client):
    response = api_client.get(f"{BASE_URL}/products/categories")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) == 4, f"Ожидали 4 категории, получили {len(categories)}"
    assert "electronics" in categories
    assert "jewelery" in categories


def test_get_products_by_category(api_client):
    category = "electronics"
    response = api_client.get(f"{BASE_URL}/products/category/{category}")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    products = response.json()
    assert len(products) > 0, "Список товаров категории пуст"

    for product in products:
        assert product["category"] == category, f"Товар {product['id']} имеет категорию {product['category']}"


def test_get_products_with_limit(api_client):
    response = api_client.get(f"{BASE_URL}/products", params={"limit": 5})

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    products = response.json()
    assert len(products) == 5, f"Ожидали 5 товаров, получили {len(products)}"


def test_get_products_sorted_desc(api_client):
    response = api_client.get(f"{BASE_URL}/products", params={"sort": "desc"})

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
    products = response.json()
    ids = [p["id"] for p in products]
    assert ids == sorted(ids, reverse=True), f"ID не отсортированы по убыванию: {ids}"


def test_product_rating_structure(api_client):
    response = api_client.get(f"{BASE_URL}/products/1")
    rating = response.json()["rating"]

    assert isinstance(rating, dict), f"rating должен быть объектом, получен {type(rating)}"
    assert "rate" in rating and "count" in rating, f"В rating нет нужных полей: {rating}"
    assert isinstance(rating["rate"], (int, float)), f"rate должен быть числом, получен {type(rating['rate'])}"
    assert isinstance(rating["count"], int), f"count должен быть int, получен {type(rating['count'])}"
    assert 0 <= rating["rate"] <= 5, f"rate вне диапазона 0–5: {rating['rate']}"
