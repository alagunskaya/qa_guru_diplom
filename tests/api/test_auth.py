import allure
from tests.config import BASE_URL
from tests.helpers import assert_status, assert_json_content_type


@allure.epic("FakeStoreAPI")
@allure.feature("Авторизация")
class TestLogin:

    @allure.story("Успешная авторизация")
    @allure.title("Вход с валидными данными возвращает 201")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self, api_client, test_user):
        with allure.step("Отправить POST /auth/login с валидными данными"):
            response = api_client.post(f"{BASE_URL}/auth/login", json=test_user)

        with allure.step("Проверить статус-код 201"):
            assert_status(response, 201)

        with allure.step("Проверить заголовок Content-Type"):
            assert_json_content_type(response)

        with allure.step("Проверить наличие и структуру JWT-токена"):
            data = response.json()
            assert "token" in data, f"Нет токена в ответе: {data}"
            assert isinstance(data["token"], str) and data["token"], "Токен пустой"
            assert data["token"].count(".") == 2, "Токен не JWT"

    @allure.story("Ошибки авторизации")
    @allure.title("Вход с неверным паролем возвращает 401")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, api_client, test_user):
        with allure.step("Отправить POST /auth/login с неверным паролем"):
            bad_creds = {"username": test_user["username"], "password": "WrongPassword1234"}
            response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

        with allure.step("Проверить статус-код 401 и сообщение об ошибке"):
            assert_status(response, 401)
            assert response.text == "username or password is incorrect"

    @allure.story("Ошибки авторизации")
    @allure.title("Вход с несуществующим username возвращает 401")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_username(self, api_client):
        with allure.step("Отправить POST /auth/login с несуществующим username"):
            bad_creds = {"username": "Some_user_123", "password": "Some_Password"}
            response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

        with allure.step("Проверить статус-код 401 и сообщение об ошибке"):
            assert_status(response, 401)
            assert response.text == "username or password is incorrect"

    @allure.story("Валидация полей")
    @allure.title("Вход без пароля возвращает 400")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_password(self, api_client, test_user):
        with allure.step("Отправить POST /auth/login без поля password"):
            bad_creds = {"username": test_user["username"]}
            response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

        with allure.step("Проверить статус-код 400 и сообщение об ошибке"):
            assert_status(response, 400)
            assert response.text == "username and password are not provided in JSON format"

    @allure.story("Валидация полей")
    @allure.title("Вход без username возвращает 400")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_username(self, api_client, test_user):
        with allure.step("Отправить POST /auth/login без поля username"):
            bad_creds = {"password": test_user["password"]}
            response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

        with allure.step("Проверить статус-код 400 и сообщение об ошибке"):
            assert_status(response, 400)
            assert response.text == "username and password are not provided in JSON format"

    @allure.story("Валидация полей")
    @allure.title("Пустое тело запроса возвращает 400")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_empty_body(self, api_client):
        with allure.step("Отправить POST /auth/login с пустым JSON"):
            response = api_client.post(f"{BASE_URL}/auth/login", json={})

        with allure.step("Проверить статус-код 400 и сообщение об ошибке"):
            assert_status(response, 400)
            assert response.text == "username and password are not provided in JSON format"
