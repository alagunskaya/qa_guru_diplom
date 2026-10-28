import allure
from jsonschema import validate
from tests.config import BASE_URL
from schemas.cart_schema import CART_CREATE_SCHEMA
from tests.helpers import assert_status


@allure.epic("FakeStoreAPI")
@allure.feature("Корзины")
class TestCartsCrud:

    @allure.story("Создание (POST)")
    @allure.title("Успешное создание корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_cart_success(self, api_client):
        payload = {
            "userId": 1,
            "products": [
                {"productId": 1, "quantity": 2},
                {"productId": 2, "quantity": 1}
            ]
        }

        with allure.step("Отправить POST /carts с валидными данными"):
            response = api_client.post(f"{BASE_URL}/carts", json=payload)

        with allure.step("Проверить статус-код 201"):
            assert_status(response, 201)

        with allure.step("Проверить, что вернулись переданные данные и сгенерированный id"):
            created = response.json()
            assert "id" in created, f"В ответе нет id: {created}"
            assert created["userId"] == payload["userId"]
            assert len(created["products"]) == len(payload["products"])

        with allure.step("Провалидировать ответ по JSON-схеме создания"):
            validate(instance=created, schema=CART_CREATE_SCHEMA)

    @allure.story("Обновление (PUT)")
    @allure.title("Успешное обновление корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_cart_success(self, api_client):
        payload = {
            "userId": 1,
            "products": [
                {"productId": 3, "quantity": 5}
            ]
        }

        with allure.step("Отправить PUT /carts/1 с новыми данными"):
            response = api_client.put(f"{BASE_URL}/carts/1", json=payload)

        with allure.step("Проверить статус-код 200"):
            assert_status(response, 200)

        with allure.step("Проверить, что данные обновились"):
            updated = response.json()
            assert updated["userId"] == payload["userId"]
            assert len(updated["products"]) == 1
            assert updated["products"][0]["productId"] == 3

    @allure.story("Создание (POST)")
    @allure.title("Создание корзины с невалидным JSON")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_cart_invalid_json(self, api_client):
        payload = "invalid_json_string"

        with allure.step("Отправить POST /carts с невалидным типом данных"):
            response = api_client.post(
                f"{BASE_URL}/carts",
                data=payload,
                headers={"Content-Type": "application/json"}
            )

        with allure.step("Проверить статус-код 400"):
            assert_status(response, 400)
