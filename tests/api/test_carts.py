import allure
import pytest
import logging
from jsonschema import validate
from tests.api.conftest import build_url
from schemas.cart_schema import CARTS_LIST_SCHEMA, CART_SCHEMA
from tests.helpers import assert_status

logger = logging.getLogger(__name__)


@allure.epic("FakeStoreAPI")
@allure.feature("Корзины")
class TestCarts:

    @allure.story("Чтение (GET)")
    @allure.title("Список всех корзин соответствует схеме")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_carts_matches_schema(self, api_client):
        with allure.step("Отправить GET /carts"):
            response = api_client.get(build_url("/carts"))

        with allure.step("Проверить статус-код 200"):
            assert_status(response, 200)

        with allure.step("Провалидировать ответ по JSON-схеме"):
            validate(instance=response.json(), schema=CARTS_LIST_SCHEMA)

    @allure.story("Чтение (GET)")
    @allure.title("Получение одной корзины по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_cart_matches_schema(self, api_client):
        with allure.step("Отправить GET /carts/1"):
            response = api_client.get(build_url("/carts/1"))

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
            response = api_client.get(build_url(f"/carts/user/{user_id}"))

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
            response = api_client.get(build_url("/carts/user/999"))

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
            products_response = api_client.get(build_url("/products"))
            existing_ids = {p["id"] for p in products_response.json()}

        with allure.step("Получить список всех корзин"):
            carts_response = api_client.get(build_url("/carts"))
            carts = carts_response.json()

        with allure.step("Проверить, что каждый productId в корзинах существует"):
            for cart in carts:
                for item in cart["products"]:
                    assert item[
                               "productId"] in existing_ids, f"В корзине {cart['id']} несуществующий товар {item['productId']}"

    @allure.story("Параметры запроса")
    @allure.title("Ограничение количества возвращаемых корзин (limit)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_carts_with_limit(self, api_client):
        with allure.step("Отправить GET /carts с параметром limit=3"):
            response = api_client.get(build_url(f"/carts"), params={"limit": 3})

        with allure.step("Проверить статус-код 200"):
            assert_status(response, 200)

        with allure.step("Проверить, что вернулось ровно 3 корзины"):
            carts = response.json()
            logger.info(f"Вернулось корзин: {len(carts)}. ID: {[c['id'] for c in carts]}")
            assert len(carts) == 3, f"Ожидали 3 корзины, получили {len(carts)}"
