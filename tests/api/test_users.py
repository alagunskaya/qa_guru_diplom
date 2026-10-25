from tests.config import BASE_URL


def test_get_users_returns_list(api_client):
    response = api_client.get(f"{BASE_URL}/users")

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

    users = response.json()
    assert isinstance(users, list), f"Ожидали список, получили {type(users)}"
    assert len(users) > 0, "Список пользователей пуст"

    print("\nСписок доступных пользователей:")
    for user in users:
        print(f"id={user['id']}, username={user['username']}, password={user.get('password', 'N/A')}")

    usernames = [u["username"] for u in users]
    assert "mor_2314" in usernames, f"mor_2314 не найден. Доступные: {usernames}"
