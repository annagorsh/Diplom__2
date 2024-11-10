from random import randint
from links import *
import allure
import requests


class TestChangeUserData:

    @allure.title("Проверяем, что можно изменить email+имя")
    def test_change_data_authorized_success(self,payload, rand_name):
        response = requests.post(CREATE_USER_URL, data=payload)
        assert response.status_code == 200 and "accessToken" in response.text
        token = response.json().get("accessToken")
        email = str(randint(10000, 99999)) + "@gmail.com"
        name = rand_name
        patch_response = requests.patch(AUTH_USER_URL,
                                         headers={"Authorization": token},
                                         data={"email": email,
                                               "name": name})
        assert patch_response.status_code == 200 and email, name in patch_response.text
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202

    @allure.title("Проверяем, что можно изменить только email")
    def test_change_email_authorized_success(self, payload):
        response = requests.post(CREATE_USER_URL, data=payload)
        assert response.status_code == 200 and "accessToken" in response.text
        token = response.json().get("accessToken")
        email = str(randint(10000, 99999)) + "@gmail.com"
        patch_response = requests.patch(AUTH_USER_URL,
                                        headers={"Authorization": token},
                                        data={"email": email})
        assert patch_response.status_code == 200 and email in patch_response.text
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202

    @allure.title("Проверяем, что можно изменить только Имя")
    def test_change_name_authorized_success(self, payload, rand_name):
        response = requests.post(CREATE_USER_URL, data=payload)
        assert response.status_code == 200 and "accessToken" in response.text
        token = response.json().get("accessToken")
        name = rand_name
        patch_response = requests.patch(AUTH_USER_URL,
                                        headers={"Authorization": token},
                                        data={"name": name})
        assert patch_response.status_code == 200 and name in patch_response.text
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202


    @allure.title("Проверяем, что нельзя изменить данные пользователя без авторизации")
    def test_change_data_unauthorized_returns_error(self, rand_name):
        response = requests.patch(
            AUTH_USER_URL,
            data={
                "email": str(randint(10000, 99999)) + "@gmail.com",
                "name": rand_name
            })
        assert response.status_code == 401 and "You should be authorised" in response.text

    @allure.title("Проверяем, что нельзя изменить email пользователя без авторизации")
    def test_change_email_unauthorized_returns_error(self):
        response = requests.patch(
            AUTH_USER_URL,
            data={
                "email": str(randint(10000, 99999)) + "@gmail.com"
            })
        assert response.status_code == 401 and "You should be authorised" in response.text

    @allure.title("Проверяем, что нельзя изменить имя пользователя без авторизации")
    def test_change_name_unauthorized_returns_error(self, rand_name):
        response = requests.patch(
            AUTH_USER_URL,
            data={
                "name": rand_name
            })
        assert response.status_code == 401 and "You should be authorised" in response.text