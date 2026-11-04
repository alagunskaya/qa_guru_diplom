import allure
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@allure.epic("Demoblaze UI")
@allure.feature("Корзина")
class TestCartUI:

    @allure.story("Добавление товара")
    @allure.title("Добавление товара в корзину и проверка наличия")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("UI", "Cart")
    def test_add_product_to_cart(self, driver):
        main_page = MainPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()
            main_page.wait_for_products_to_load()

        with allure.step("Перейти на страницу товара 'Samsung galaxy s6'"):
            main_page.select_product("Samsung galaxy s6")

        with allure.step("Добавить товар в корзину"):
            product_page.click_add_to_cart()

        with allure.step("Перейти в корзину"):
            main_page.click_cart_nav()

        with allure.step("Проверить, что товар отображается в корзине"):
            cart_page.should_have_product("Samsung galaxy s6")

    @allure.story("Пустая корзина")
    @allure.title("Проверка пустой корзины")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("UI", "Cart")
    def test_empty_cart(self, driver):
        main_page = MainPage(driver)
        cart_page = CartPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Перейти в корзину без добавления товаров"):
            main_page.click_cart_nav()

        with allure.step("Проверить, что корзина пуста"):
            cart_page.should_be_empty()
