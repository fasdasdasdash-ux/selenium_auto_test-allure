import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    username = driver.find_element(By.ID, "username")
    username.send_keys("tomsmith")

    password = driver.find_element(By.ID, "password")
    password.send_keys("SuperSecretPassword!")

    login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_btn.click()

    success_message = driver.find_element(By.CSS_SELECTOR, ".flash.success")
    assert "You logged into a secure area" in success_message.text

def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    username = driver.find_element(By.ID, "username")
    username.send_keys("wronguser")

    password = driver.find_element(By.ID, "password")
    password.send_keys("wrongpass")

    login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_btn.click()

    error_message = driver.find_element(By.CSS_SELECTOR, ".flash.error")
    assert "Your username is invalid!" in error_message.text