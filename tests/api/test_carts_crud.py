import allure
from jsonschema import validate
from tests.config import BASE_URL
from schemas.cart_schema import CART_CREATE_SCHEMA


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
            assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}. Тело: {response.text}"

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
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что данные обновились"):
            updated = response.json()
            assert updated["userId"] == payload["userId"]
            assert len(updated["products"]) == 1
            assert updated["products"][0]["productId"] == 3

    @allure.story("Удаление (DELETE)")
    @allure.title("Успешное удаление корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_cart_success(self, api_client):
        with allure.step("Отправить DELETE /carts/1"):
            response = api_client.delete(f"{BASE_URL}/carts/1")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что вернулся удаленный объект"):
            deleted = response.json()
            assert deleted["id"] == 1
            assert "userId" in deleted
