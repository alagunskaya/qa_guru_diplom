import allure
from jsonschema import validate
from tests.config import BASE_URL
from schemas.product_schema import PRODUCT_CREATE_SCHEMA


@allure.epic("FakeStoreAPI")
@allure.feature("Товары")
class TestProductsCrud:

    @allure.story("Создание (POST)")
    @allure.title("Успешное создание нового товара")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_product_success(self, api_client):
        payload = {
            "title": "Test Product",
            "price": 42.5,
            "description": "API tests",
            "image": "https://i.pravatar.cc",
            "category": "electronics"
        }

        with allure.step("Отправить POST /products с валидными данными"):
            response = api_client.post(f"{BASE_URL}/products", json=payload)

        with allure.step("Проверить статус-код 201"):
            assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что вернулись переданные данные и сгенерированный id"):
            created = response.json()
            assert "id" in created, f"В ответе нет id: {created}"
            assert created["title"] == payload["title"]
            assert created["price"] == payload["price"]

        with allure.step("Провалидировать ответ по JSON-схеме создания"):
            validate(instance=created, schema=PRODUCT_CREATE_SCHEMA)

    @allure.story("Обновление (PUT)")
    @allure.title("Успешное обновление существующего товара")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_product_success(self, api_client):
        payload = {
            "title": "Updated Title",
            "price": 99.99,
            "description": "Updated description",
            "image": "https://i.pravatar.cc",
            "category": "electronics"
        }

        with allure.step("Отправить PUT /products/1 с новыми данными"):
            response = api_client.put(f"{BASE_URL}/products/1", json=payload)

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что данные обновились"):
            updated = response.json()
            assert updated["title"] == payload["title"]
            assert updated["price"] == payload["price"]

    @allure.story("Удаление (DELETE)")
    @allure.title("Успешное удаление товара")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_product_success(self, api_client):
        with allure.step("Отправить DELETE /products/1"):
            response = api_client.delete(f"{BASE_URL}/products/1")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что вернулся удаленный объект"):
            deleted = response.json()
            assert deleted["id"] == 1
            assert "title" in deleted
