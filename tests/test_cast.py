import pytest
from selenium import webdriver
from time import sleep


# Fixture for Chrome
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    c_options = webdriver.ChromeOptions()
    # All the arguments added for chromium to work on selenium
    c_options.add_argument("--no-sandbox")  # This make Chromium reachable
    c_options.add_argument("--headless")
    c_options.add_argument("--disable-gpu")
    c_options.add_argument("--no-default-browser-check")  # Overrides default choices
    c_options.add_argument("--no-first-run")
    c_options.add_argument("--disable-default-apps")
    chrome_driver = webdriver.Chrome(chrome_options=c_options, executable_path="/usr/bin/chromedriver")
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()


@pytest.mark.usefixtures("chrome_driver_init")
class BasicChromeTest:
    pass


# Test for correct html
class TestURLChrome(BasicChromeTest):
    def test_open_url(self):
        self.driver.get("http://127.0.0.1:5000")
        sleep(2.5)  # TODO:Should be implicit wait
        assert self.driver.title == "cast.sh"
