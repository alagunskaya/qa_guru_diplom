from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    CART_ITEMS = (By.CSS_SELECTOR, "#tbodyid tr")

    @allure.step("Проверить, что в корзине есть товар: {product_name}")
    def should_have_product(self, product_name):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.CART_ITEMS))
        page_source = self.driver.page_source
        assert product_name in page_source, f"Товар '{product_name}' не найден в корзине"

    @allure.step("Проверить, что корзина пуста")
    def should_be_empty(self):
        time.sleep(2)
        assert len(self.driver.find_elements(*self.CART_ITEMS)) == 0, "Корзина не пуста!"
