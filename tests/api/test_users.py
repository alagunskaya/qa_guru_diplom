import allure
from tests.config import BASE_URL


@allure.epic("FakeStoreAPI")
@allure.feature("Пользователи")
class TestUsers:

    @allure.story("Чтение (GET)")
    @allure.title("Получение списка пользователей и проверка наличия тестового аккаунта")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_users_returns_list(self, api_client):
        with allure.step("Отправить GET /users"):
            response = api_client.get(f"{BASE_URL}/users")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

        with allure.step("Проверить, что вернулся непустой список"):
            users = response.json()
            assert isinstance(users, list), f"Ожидали список, получили {type(users)}"
            assert len(users) > 0, "Список пользователей пуст"

        with allure.step("Прикрепить список пользователей к отчету"):
            users_info = "\n".join(
                [f"id={u['id']}, username={u['username']}, password={u.get('password', 'N/A')}" for u in users]
            )
            allure.attach(
                users_info,
                name="Список доступных пользователей",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверить наличие тестового пользователя mor_2314"):
            usernames = [u["username"] for u in users]
            assert "mor_2314" in usernames, f"mor_2314 не найден. Доступные: {usernames}"
