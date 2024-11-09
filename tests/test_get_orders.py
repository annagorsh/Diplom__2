import allure
import requests
from links import *

class TestGetOrders:

    @allure.title("Проверяем получение списка заказов конкретного пользователя с авторизацией")
    def test_get_users_orders_authorized_success(self, payload):
        response = requests.post(CREATE_USER_URL, data=payload)
        assert response.status_code == 200
        token = response.json().get("accessToken")
        get_order_response = requests.get(ORDER_URL,
                                          headers={"Authorization": token})
        assert get_order_response.status_code == 200 and "orders" in get_order_response.text
        delete_response = requests.delete(AUTH_USER_URL, headers={"Authorization": token})
        assert delete_response.status_code == 202

    @allure.title("Проверяем, что без авторизации нельзя получить список заказов")
    def test_get_users_orders_unauthorized_returns_error(self):
        response = requests.get(ORDER_URL)
        assert response.status_code == 401 and "You should be authorised" in response.text