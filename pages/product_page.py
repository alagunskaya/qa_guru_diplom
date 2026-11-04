from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "a.btn-success")

    @allure.step("Нажать кнопку 'Add to cart' на странице товара")
    def click_add_to_cart(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN)).click()

        # Обрабатываем alert
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert "Product added" in alert_text, f"Ожидали 'Product added', получили: {alert_text}"
        return self
