import allure
import requests
from links import *


class TestCreateOrder:

    @allure.title("Проверяем создание заказа с ингредиентами авторизованным пользователем")
    def test_create_order_authorized_success(self, payload, ingredients_list):
        response = requests.post(CREATE_USER_URL, data=payload)
        assert response.status_code == 200
        token = response.json().get("accessToken")
        order_response = requests.post(ORDER_URL,
                                       headers={"Authorization": token},
                                       json = ingredients_list)
        assert order_response.status_code == 200 and "order", "number" in order_response.text
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202

    @allure.title("Проверяем, что можно создать заказ без авторизации")
    def test_create_order_unauthorized_success(self, ingredients_list):
        response = requests.post(ORDER_URL,
                                       json=ingredients_list)
        assert response.status_code == 200 and "order", "number" in response.text

    @allure.title("Проверяем, что нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients_returns_error(self):
        response = requests.post(ORDER_URL)
        assert response.status_code == 400 and "Ingredient ids must be provided" in response.text

    @allure.title("Проверяем, что нельзя создать заказ с некорректным значением ингредиентов")
    def test_create_order_invalid_ingredients_returns_error(self, invalid_ingredients):
        response = requests.post(ORDER_URL,
                                 json=invalid_ingredients)
        assert response.status_code == 500 and "Internal Server Error" in response.text