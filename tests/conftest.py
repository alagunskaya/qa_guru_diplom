import allure
import logging
import pytest
import requests
from tests.config import BASE_URL


@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session


@pytest.fixture
def test_user(api_client):
    response = api_client.get(f"{BASE_URL}/users")
    assert response.status_code == 200, f"Не удалось получить пользователей: {response.text}"

    users = response.json()
    user = next((u for u in users if u["username"] == "mor_2314"), None)
    assert user is not None, "Пользователь mor_2314 не найден в /users"

    return {"username": user["username"], "password": user["password"]}


@pytest.fixture
def auth_client(api_client, test_user):
    response = api_client.post(f"{BASE_URL}/auth/login", json=test_user)
    assert response.status_code == 201, f"Login failed: {response.text}"

    token = response.json().get("token")
    assert token, "В ответе логина нет токена"

    api_client.headers.update({"Authorization": f"Bearer {token}"})
    return api_client


logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def log_requests(request):
    # Сохраняем оригинальный метод requests.Session.request
    original_request = requests.Session.request

    def custom_request(self, method, url, *args, **kwargs):
        # 1. Логируем запрос в консоль
        logger.info(f"Request: {method} {url}")

        # 2. Выполняем сам запрос
        response = original_request(self, method, url, *args, **kwargs)

        # 3. Логируем ответ в консоль
        logger.info(f"Response: {response.status_code} {url}")

        # 4. Прикрепляем тело запроса (если есть) в Allure
        if kwargs.get("json"):
            allure.attach(
                str(kwargs["json"]),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON
            )

        # 5. Прикрепляем тело ответа в Allure
        allure.attach(
            response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.JSON
        )

        return response

    # Подменяем оригинальный метод на наш
    requests.Session.request = custom_request

    # Отдаем управление тесту
    yield

    # После теста возвращаем всё как было
    requests.Session.request = original_request
