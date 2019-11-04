import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

# Fixture for Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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

@pytest.fixture(scope="class")
def firefox_driver_init(request):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('plugin.state.flash', 0)
    profile.update_preferences()
    firefox_driver = webdriver.Firefox(executable_path="usr/bin/geckodriver")
    request.cls.driver = firefox_driver
    yield
    firefox_driver.close()

@pytest.mark.usefixtures("chrome_driver_init")
class BasicChromeTest:
    pass

@pytest.mark.usefixtures("firefox_driver_init")
class BasicGeckoTest:
    pass


# Test for correct html
class TestCast(BasicChromeTest):
    def test_serving_app_html(self):
        self.driver.get("http://127.0.0.1:5000")
        sleep(2.5)  # TODO:Should be implicit wait
        assert self.driver.title == "cast.sh"

    def test_empty_session_log_download(self):
        self.driver.get("http://127.0.0.1:5000")
        tabs = self.driver.find_elements(By.CLASS_NAME, 'tab')
        assert len(tabs) == 1
        close_tabs = self.driver.find_elements(By.CLASS_NAME, 'close')
        assert len(close_tabs) == 1
        close_tabs[0].click()
        tabs = self.driver.find_elements(By.CLASS_NAME, 'tab')
        assert tabs[0].text == "[closed] tab 1"
        log_btn = self.driver.find_element(By.CLASS_NAME, 'log')
        log_btn.click()
        # no_log_avlble = WebDriverWait(self.driver, 6).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "notyf__message"))
        # )
        sleep(2)
        no_log_avlble = self.driver.find_element(By.CLASS_NAME, 'notyf__message')
        assert no_log_avlble.text == "No log available for download."
