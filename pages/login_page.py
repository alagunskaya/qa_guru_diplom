from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    USERNAME_INPUT = (By.ID, "loginusername")
    PASSWORD_INPUT = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Log in']")

    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        ).send_keys(username)
        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self

    @allure.step("Нажать кнопку Log in")
    def click_login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self

    @allure.step("Выполнить вход")
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self

    @allure.step("Проверить текст ошибки в модальном окне")
    def should_have_error(self, expected_text):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        actual_text = alert.text
        alert.accept()
        assert expected_text in actual_text, f"Ожидали ошибку '{expected_text}', получили: '{actual_text}'"
