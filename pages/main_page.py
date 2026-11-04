from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.demoblaze.com/"

    LOGIN_NAV_BUTTON = (By.ID, "login2")
    CART_NAV_BUTTON = (By.ID, "cartur")
    WELCOME_TEXT = (By.ID, "nameofuser")

    @allure.step("Открыть главную страницу Demoblaze")
    def open(self):
        self.driver.get(self.url)
        return self

    @allure.step("Нажать кнопку 'Log in' в навигации")
    def click_login_nav(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_NAV_BUTTON)
        ).click()
        return self

    @allure.step("Проверить, что пользователь {username} успешно авторизован")
    def should_have_logged_in_user(self, username):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.WELCOME_TEXT))
        assert f"Welcome {username}" in element.text, f"Ожидали 'Welcome {username}', получили: {element.text}"

    @allure.step("Нажать кнопку 'Cart' в навигации")
    def click_cart_nav(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CART_NAV_BUTTON)
        ).click()
        return self

    @allure.step("Дождаться загрузки карточек товаров")
    def wait_for_products_to_load(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card")))
        return self

    @allure.step("Кликнуть на товар: {product_name}")
    def select_product(self, product_name):
        product_link = (By.LINK_TEXT, product_name)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(product_link)).click()
        return self

    @allure.step("Кликнуть на категорию: {category_name}")
    def click_category(self, category_name):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, category_name))).click()
        return self

    @allure.step("Проверить, что в списке отображаются только товары категории")
    def should_display_category_items(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card-title")))
        page_source = self.driver.page_source
        assert "Samsung galaxy s6" in page_source, "Не найден телефон Samsung"
        assert "MacBook air" not in page_source, "В категории телефонов найден ноутбук"
