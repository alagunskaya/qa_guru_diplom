import allure
from jsonschema import validate
from tests.config import BASE_URL
from schemas.product_schema import PRODUCTS_LIST_SCHEMA, PRODUCT_SCHEMA


@allure.epic("FakeStoreAPI")
@allure.feature("Товары")
class TestProducts:

    @allure.story("Чтение (GET)")
    @allure.title("Получение списка товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_products(self, api_client):
        with allure.step("Отправить GET /products"):
            response = api_client.get(f"{BASE_URL}/products")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что вернулось ровно 20 товаров"):
            products = response.json()
            assert len(products) == 20, f"Ожидали 20 товаров, получили {len(products)}"

    @allure.story("Валидация схемы")
    @allure.title("Список товаров соответствует JSON-схеме")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_products_matches_schema(self, api_client):
        with allure.step("Отправить GET /products"):
            response = api_client.get(f"{BASE_URL}/products")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

        with allure.step("Провалидировать список по JSON-схеме"):
            products = response.json()
            validate(instance=products, schema=PRODUCTS_LIST_SCHEMA)

    @allure.story("Валидация схемы")
    @allure.title("Один товар соответствует JSON-схеме")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_product_matches_schema(self, api_client):
        with allure.step("Отправить GET /products/1"):
            response = api_client.get(f"{BASE_URL}/products/1")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200

        with allure.step("Провалидировать товар по JSON-схеме"):
            product = response.json()
            validate(instance=product, schema=PRODUCT_SCHEMA)

    @allure.story("Бизнес-логика")
    @allure.title("ID всех товаров уникальны")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_products_unique_ids(self, api_client):
        with allure.step("Отправить GET /products"):
            response = api_client.get(f"{BASE_URL}/products")
            products = response.json()

        with allure.step("Проверить, что нет дублирующихся ID"):
            ids = [p["id"] for p in products]
            assert len(ids) == len(set(ids)), f"Найдены дубли ID: {ids}"

    @allure.story("Чтение (GET)")
    @allure.title("Получение конкретного товара по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_product_success(self, api_client):
        with allure.step("Отправить GET /products/1"):
            response = api_client.get(f"{BASE_URL}/products/1")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить поля конкретного товара"):
            product = response.json()
            assert product["id"] == 1
            assert product["title"] == "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"
            assert product["price"] == 109.95
            assert product["category"] == "men's clothing"

    @allure.story("Чтение (GET)")
    @allure.title("Запрос несуществующего товара возвращает пустое тело")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_single_product_not_found(self, api_client):
        with allure.step("Отправить GET /products/999"):
            response = api_client.get(f"{BASE_URL}/products/999")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

        with allure.step("Проверить, что тело ответа пустое"):
            assert response.text == "", f"Ожидали пустое тело, получили: {response.text}"

    @allure.story("Фильтрация")
    @allure.title("Получение списка категорий")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_categories(self, api_client):
        with allure.step("Отправить GET /products/categories"):
            response = api_client.get(f"{BASE_URL}/products/categories")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить структуру и наличие 4 категорий"):
            categories = response.json()
            assert isinstance(categories, list)
            assert len(categories) == 4, f"Ожидали 4 категории, получили {len(categories)}"
            assert "electronics" in categories
            assert "jewelery" in categories

    @allure.story("Фильтрация")
    @allure.title("Получение товаров определенной категории")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category(self, api_client):
        category = "electronics"

        with allure.step(f"Отправить GET /products/category/{category}"):
            response = api_client.get(f"{BASE_URL}/products/category/{category}")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"
            products = response.json()

        with allure.step("Проверить, что список не пуст и все товары нужной категории"):
            assert len(products) > 0, "Список товаров категории пуст"
            for product in products:
                assert product["category"] == category, f"Товар {product['id']} имеет категорию {product['category']}"

    @allure.story("Параметры запроса")
    @allure.title("Ограничение количества возвращаемых товаров (limit)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_with_limit(self, api_client):
        with allure.step("Отправить GET /products с параметром limit=5"):
            response = api_client.get(f"{BASE_URL}/products", params={"limit": 5})

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что вернулось ровно 5 товаров"):
            products = response.json()
            assert len(products) == 5, f"Ожидали 5 товаров, получили {len(products)}"

    @allure.story("Параметры запроса")
    @allure.title("Сортировка товаров по убыванию ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_sorted_desc(self, api_client):
        with allure.step("Отправить GET /products с параметром sort=desc"):
            response = api_client.get(f"{BASE_URL}/products", params={"sort": "desc"})

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что ID отсортированы по убыванию"):
            products = response.json()
            ids = [p["id"] for p in products]
            assert ids == sorted(ids, reverse=True), f"ID не отсортированы по убыванию: {ids}"

    @allure.story("Бизнес-логика")
    @allure.title("Проверка структуры и диапазона рейтинга товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_rating_structure(self, api_client):
        with allure.step("Отправить GET /products/1"):
            response = api_client.get(f"{BASE_URL}/products/1")
            rating = response.json()["rating"]

        with allure.step("Проверить структуру вложенного объекта rating"):
            assert isinstance(rating, dict), f"rating должен быть объектом, получен {type(rating)}"
            assert "rate" in rating and "count" in rating, f"В rating нет нужных полей: {rating}"

        with allure.step("Проверить типы данных и диапазон значений"):
            assert isinstance(rating["rate"], (int, float)), f"rate должен быть числом, получен {type(rating['rate'])}"
            assert isinstance(rating["count"], int), f"count должен быть int, получен {type(rating['count'])}"
            assert 0 <= rating["rate"] <= 5, f"rate вне диапазона 0–5: {rating['rate']}"
