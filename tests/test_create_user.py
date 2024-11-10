import requests
import allure

from links import *


class TestCreateUser:

    @allure.title("Проверяем, что пользователь успешно создан и затем удаляем его")
    def test_user_is_successfully_created(self, payload):
        response = requests.post(CREATE_USER_URL, data = payload)
        assert response.status_code == 200 and "accessToken" in response.text
        token = response.json().get("accessToken")
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202

    @allure.title("Проверяем, что нельзя создать пользователя, если такой уже зарегистрирован")
    def test_cannot_create_existing_user(self, payload):
        user_data = payload
        response1 = requests.post(CREATE_USER_URL, data=user_data)
        assert response1.status_code == 200
        response2 = requests.post(CREATE_USER_URL, data=user_data)
        assert response2.status_code == 403 and "User already exists" in response2.text
        token = response1.json().get("accessToken")
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202

    @allure.title("Проверяем, что нельзя создать пользователя, передав не все параметры")
    def test_cannot_create_user_without_all_necessary_params(self, incomplete_user_data):
        response = requests.post(CREATE_USER_URL, data=incomplete_user_data)
        assert response.status_code == 403 and "Email, password and name are required fields" in response.text

