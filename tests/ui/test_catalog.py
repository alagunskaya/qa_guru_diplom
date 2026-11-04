import allure
from pages.main_page import MainPage


@allure.epic("Demoblaze UI")
@allure.feature("Каталог")
class TestCatalogUI:

    @allure.story("Фильтрация")
    @allure.title("Фильтрация товаров по категории 'Phones'")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("UI", "Catalog")
    def test_filter_by_phones_category(self, driver):
        main_page = MainPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()
            main_page.wait_for_products_to_load()

        with allure.step("Кликнуть на категорию 'Phones'"):
            main_page.click_category("Phones")

        with allure.step("Проверить, что отображаются только телефоны"):
            main_page.should_display_category_items()
