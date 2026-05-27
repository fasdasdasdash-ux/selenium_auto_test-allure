import pytest
import allure

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    with allure.step("Запустить браузер Chrome в headless-режиме"):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
    yield driver
    with allure.step("Закрыть браузер"):
        driver.quit()


@allure.title("Успешная авторизация")
@allure.description(
    "Тест проверяет, что пользователь может войти с валидными данными (логин: tomsmith, пароль: SuperSecretPassword!)")
@allure.feature("Авторизация")
@allure.story("Позитивный сценарий")
def test_successful_login(driver):
    with allure.step("Открыть страницу авторизации"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Ввести логин 'tomsmith'"):
        username = driver.find_element(By.ID, "username")
        username.send_keys("tomsmith")

    with allure.step("Ввести пароль 'SuperSecretPassword!'"):
        password = driver.find_element(By.ID, "password")
        password.send_keys("SuperSecretPassword!")

    with allure.step("Нажать кнопку 'Login'"):
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()

    with allure.step("Проверить, что отображается сообщение об успешном входе"):
        success_message = driver.find_element(By.CSS_SELECTOR, ".flash.success")
        assert "You logged into a secure area" in success_message.text


@allure.title("Неуспешная авторизация")
@allure.description(
    "Тест проверяет, что при вводе неверных данных пользователь не может войти и видит сообщение об ошибке")
@allure.feature("Авторизация")
@allure.story("Негативный сценарий")
def test_unsuccessful_login(driver):
    with allure.step("Открыть страницу авторизации"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Ввести неверный логин 'wronguser'"):
        username = driver.find_element(By.ID, "username")
        username.send_keys("wronguser")

    with allure.step("Ввести неверный пароль 'wrongpass'"):
        password = driver.find_element(By.ID, "password")
        password.send_keys("wrongpass")

    with allure.step("Нажать кнопку 'Login'"):
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()

    with allure.step("Проверить, что отображается сообщение об ошибке"):
        error_message = driver.find_element(By.CSS_SELECTOR, ".flash.error")
        assert "Your username is invalid!" in error_message.text