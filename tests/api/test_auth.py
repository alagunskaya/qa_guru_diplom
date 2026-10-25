from tests.config import BASE_URL


def test_login_success(api_client, test_user):
    response = api_client.post(f"{BASE_URL}/auth/login", json=test_user)

    assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}. Тело: {response.text}"

    data = response.json()
    assert "token" in data, f"Нет токена в ответе: {data}"
    assert isinstance(data["token"], str) and data["token"], "Токен пустой"
    assert data["token"].count(".") == 2, "Токен не JWT"


def test_login_wrong_password(api_client, test_user):
    bad_creds = {"username": test_user["username"], "password": "WrongPassword123"}

    response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

    assert response.status_code == 401, f"Ожидали 401, получили {response.status_code}. Тело: {response.text}"
    assert response.text == "username or password is incorrect"


def test_login_wrong_username(api_client):
    bad_creds = {"username": "Some_user_1", "password": "Some_Password"}

    response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

    assert response.status_code == 401, f"Ожидали 401, получили {response.status_code}. Тело: {response.text}"
    assert response.text == "username or password is incorrect"


def test_login_missing_password(api_client, test_user):
    bad_creds = {"username": test_user["username"]}

    response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Тело: {response.text}"
    assert response.text == "username and password are not provided in JSON format"


def test_login_missing_username(api_client, test_user):
    bad_creds = {"password": test_user["password"]}

    response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Тело: {response.text}"
    assert response.text == "username and password are not provided in JSON format"


def test_login_empty_body(api_client):
    response = api_client.post(f"{BASE_URL}/auth/login", json={})

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Тело: {response.text}"
    assert response.text == "username and password are not provided in JSON format"
