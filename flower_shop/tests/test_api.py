from rest_framework.test import APITestCase
from ..models import CategoryPrice, Reason
from rest_framework.status import HTTP_200_OK
from ..serializer import CategoryPriceSerializer
from django.core.exceptions import ObjectDoesNotExist
import requests
from django.contrib.auth.models import User
import pytest


import pytest
from rest_framework.test import APIClient
from ..models import CategoryPrice


# @pytest.fixture
# def client():
#     return APIClient()
#
# @pytest.mark.django_db
# class Test_Flower_shopApi:
#     endpoint = '/categories/send/'
#
#     def test_new_db(self, client):
#         CategoryPrice.objects.create(name='до 1500$')
#         CategoryPrice.objects.create(name='хрень всякая')
#         response = client.get(self.endpoint)
#         assert response.json() == {'categories': ['до 1500$', 'хрень всякая']}
#
#     def test_current_db(self, client):
#         CategoryPrice.objects.create(name='до 1500$')
#         CategoryPrice.objects.create(name='хрень всякая')
#         response = client.get(self.endpoint)
#         assert response.json() == {'categories': ['до 500р',
#                                                   '500 -  1000р',
#                                                   '1000 - 2000р',
#                                                   'более 2000р',
#                                                   'до 1500$',
#                                                   'хрень всякая']}



# class Flower_shopApiTestCase(APITestCase):
#     def test_get(self):
#         CategoryPrice.objects.create(name='до 1500$')
#         CategoryPrice.objects.create(name='хрень всякая')
#         url = "http://127.0.0.1:8000/categories/send/"
#         response = self.client.get(url)
#         assert response.status_code == HTTP_200_OK
#         assert response.json() == {'categories': ['до 1500$', 'хрень всякая']}
#
#     def test_get_with_serializer(self):
#         category_1 = CategoryPrice.objects.create(name='до 1500$')
#         category_2 = CategoryPrice.objects.create(name='хрень всякая')
#         url = "http://127.0.0.1:8000/categories/test/send/"
#         response = self.client.get(url)
#         serializer_data = CategoryPriceSerializer([category_1, category_2], many=True).data
#         assert response.data == serializer_data
#
#     def test_create_user_apitestcase(self):
#         user_test = User.objects.create_user('user1', 'myemail@crazymail.com', 'user1')
#         user_test.first_name = 'John'
#         user_test.last_name = 'Citizen'
#         user_test.save()
#         user_check = User.objects.get(username='user1')
#         assert user_check.last_name == 'Citizen', 'имя не прошло'
#         assert user_check.email == 'myemail@crazymail.com', 'пользователь не создан'
#
#
# def test_category_price():
#     url = "http://127.0.0.1:8000/categories/send/"
#     response = requests.get(url)
#     assert response.json() == {'categories': ['до 500р', '500 -  1000р', '1000 - 2000р', 'более 2000р']}
#
#
#
# @pytest.mark.django_db
# def test_create_user_pytest():
#     user_test = User.objects.create_user('user1', 'myemail@crazymail.com', 'user1')
#     user_test.first_name = 'John'
#     user_test.last_name = 'Citizen'
#     user_test.save()
#     user_check = User.objects.get(username='user1')
#     assert user_check.last_name == 'Citizen', 'имя не прошло'
#     assert user_check.email == 'myemail@crazymail.com', 'пользователь не создан'


# @pytest.mark.django_db
# @pytest.mark.parametrize('expected_exception, model',
#                          [(ObjectDoesNotExist, Reason),
#                           (ObjectDoesNotExist, CategoryPrice)])
# def test_noexist_object_error(expected_exception, model):
#     with pytest.raises(expected_exception):
#         model.objects.get(name='День рождения')


# @pytest.mark.django_db
# def test_serializer():
#     category_1 = CategoryPrice.objects.create(name='до 1500$')
#     category_2 = CategoryPrice.objects.create(name='хрень всякая')
#     serializer_data = CategoryPriceSerializer([category_1, category_2], many=True).data
#     expected_data = [
#         {
#             'id': category_1.id,
#             'name': 'до 1500$'
#         },
#         {
#             'id': category_2.id,
#             'name': 'хрень всякая'
#         }
#     ]
#     print(serializer_data)
#     assert expected_data == serializer_data