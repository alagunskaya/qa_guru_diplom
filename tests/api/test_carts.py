import allure
import pytest
from jsonschema import validate
from tests.config import BASE_URL
from schemas.cart_schema import CARTS_LIST_SCHEMA, CART_SCHEMA
from tests.helpers import assert_status


@allure.epic("FakeStoreAPI")
@allure.feature("Корзины")
class TestCarts:

    @allure.story("Чтение (GET)")
    @allure.title("Список всех корзин соответствует схеме")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_carts_matches_schema(self, api_client):
        with allure.step("Отправить GET /carts"):
            response = api_client.get(f"{BASE_URL}/carts")

        with allure.step("Проверить статус-код 200"):
            assert_status(response, 200)

        with allure.step("Провалидировать ответ по JSON-схеме"):
            validate(instance=response.json(), schema=CARTS_LIST_SCHEMA)

    @allure.story("Чтение (GET)")
    @allure.title("Получение одной корзины по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_cart_matches_schema(self, api_client):
        with allure.step("Отправить GET /carts/1"):
            response = api_client.get(f"{BASE_URL}/carts/1")

        with allure.step("Проверить статус-код 200"):
            assert_status(response, 200)

        with allure.step("Провалидировать ответ по JSON-схеме корзины"):
            cart = response.json()
            validate(instance=cart, schema=CART_SCHEMA)

        with allure.step("Проверить, что ID корзины равен 1"):
            assert cart["id"] == 1

    @allure.story("Фильтрация")
    @allure.title("Получение корзин по ID пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_id", [1, 2, 3, 8])
    def test_get_carts_by_user(self, api_client, user_id):
        with allure.step(f"Отправить GET /carts/user/{user_id}"):
            response = api_client.get(f"{BASE_URL}/carts/user/{user_id}")

        with allure.step(f"Проверить статус-код 200 и наличие корзин"):
            assert_status(response, 200)
            carts = response.json()
            assert len(carts) > 0, f"У пользователя {user_id} нет корзин"

        with allure.step(f"Проверить, что все корзины принадлежат пользователю {user_id}"):
            for cart in carts:
                assert cart["userId"] == user_id, f"Корзина {cart['id']} принадлежит {cart['userId']}, а не {user_id}"

    @allure.story("Фильтрация")
    @allure.title("Запрос корзин для несуществующего пользователя")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_carts_for_nonexistent_user(self, api_client):
        with allure.step("Отправить GET /carts/user/999"):
            response = api_client.get(f"{BASE_URL}/carts/user/999")

        with allure.step("Проверить статус-код 200"):
            assert_status(response, 200)

        with allure.step("Проверить, что вернулся пустой массив"):
            carts = response.json()
            assert carts == [], f"Ожидали пустой список, получили {carts}"

    @allure.story("Интеграция")
    @allure.title("Все товары в корзинах ссылаются на существующие товары")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_products_reference_existing_products(self, api_client):
        with allure.step("Получить список ID всех существующих товаров"):
            products_response = api_client.get(f"{BASE_URL}/products")
            existing_ids = {p["id"] for p in products_response.json()}

        with allure.step("Получить список всех корзин"):
            carts_response = api_client.get(f"{BASE_URL}/carts")
            carts = carts_response.json()

        with allure.step("Проверить, что каждый productId в корзинах существует"):
            for cart in carts:
                for item in cart["products"]:
                    assert item["productId"] in existing_ids, f"В корзине {cart['id']} несуществующий товар {item['productId']}"

    @allure.story("Бизнес-логика")
    @allure.title("Количество товара в корзинах всегда положительное")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_quantities_are_positive(self, api_client):
        with allure.step("Получить список всех корзин"):
            response = api_client.get(f"{BASE_URL}/carts")
            carts = response.json()

        with allure.step("Проверить, что quantity > 0 для всех товаров"):
            for cart in carts:
                for item in cart["products"]:
                    assert item["quantity"] > 0, f"Корзина {cart['id']}, товар {item['productId']}: количество={item['quantity']}"
