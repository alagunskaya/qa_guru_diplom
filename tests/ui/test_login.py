import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage


@allure.epic("Demoblaze UI")
@allure.feature("Авторизация")
class TestLoginUI:

    @allure.story("Успешный вход")
    @allure.title("Вход с валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("UI", "Login")
    def test_successful_login(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        with allure.step("Открыть главную страницу и нажать 'Log in'"):
            main_page.open().click_login_nav()

        with allure.step("Ввести валидные данные и войти"):
            login_page.login("test", "test")

        with allure.step("Проверить, что вход выполнен успешно"):
            main_page.should_have_logged_in_user("test")

    @allure.story("Негативные сценарии")
    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("UI", "Login", "Negative")
    def test_login_wrong_password(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        with allure.step("Открыть главную страницу и нажать 'Log in'"):
            main_page.open().click_login_nav()

        with allure.step("Ввести неверный пароль и войти"):
            login_page.login("test", "wrong_password")

        with allure.step("Проверить, что появилась ошибка"):
            login_page.should_have_error("Wrong password.")

    @allure.story("Негативные сценарии")
    @allure.title("Вход с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("UI", "Login", "Negative")
    def test_login_empty_fields(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        with allure.step("Открыть главную страницу и нажать 'Log in'"):
            main_page.open().click_login_nav()

        with allure.step("Нажать 'Log in' без ввода данных"):
            login_page.click_login_button()

        with allure.step("Проверить, что появилась ошибка"):
            login_page.should_have_error("Please fill out Username and Password.")
