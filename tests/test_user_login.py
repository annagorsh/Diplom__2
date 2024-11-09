from random import randint

import allure
import requests

from links import *


class TestUserLogin:

    @allure.title("Проверяем логин под данными существующего пользователя")
    def test_login_valid_user_success(self, payload):
        response = requests.post(CREATE_USER_URL, data=payload)
        assert response.status_code == 200
        email = payload.get("email")
        password = payload.get("password")
        response = requests.post(LOGIN_URL,
                                 data={"email": email,
                                       "password": password})
        assert response.status_code == 200 and "name" in response.text
        token = response.json().get("accessToken")
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202

    @allure.title("Проверяем логин под данными несуществующего пользователя")
    def test_login_nonexistent_data(self):
        response = requests.post(
            LOGIN_URL,
            data={
                "email": str(randint(10000, 99999)) + "@gmail.com",
                "password": str(randint(1000000, 9999999))
            }
        )
        assert response.status_code == 401 and "incorrect" in response.text