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
    assert response.status_code == 200, f"Login failed: {response.text}"

    token = response.json().get("token")
    assert token, "В ответе логина нет токена"

    api_client.headers.update({"Authorization": f"Bearer {token}"})
    return api_client
