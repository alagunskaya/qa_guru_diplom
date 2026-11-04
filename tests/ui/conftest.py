import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

from utils import attach

load_dotenv()

SELENOID_LOGIN = os.getenv("SELENOID_LOGIN")
SELENOID_PASSWORD = os.getenv("SELENOID_PASSWORD")
SELENOID_URL = os.getenv("SELENOID_URL")


@pytest.fixture(scope="function")
def driver(request):
    use_selenoid = request.config.getoption("--selenoid", default=False)

    if use_selenoid:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.set_capability("browserName", "chrome")
        options.set_capability("browserVersion", "148.0")
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": True
        })

        driver = webdriver.Remote(
            command_executor=f"https://{SELENOID_LOGIN}:{SELENOID_PASSWORD}@{SELENOID_URL}/wd/hub",
            options=options
        )
    else:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(5)
    yield driver

    attach.add_screenshot(driver)
    attach.add_page_source(driver)
    attach.add_logs(driver)
    if use_selenoid:
        attach.add_video(driver)

    driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--selenoid",
        action="store_true",
        default=False,
        help="Run tests in Selenoid"
    )
