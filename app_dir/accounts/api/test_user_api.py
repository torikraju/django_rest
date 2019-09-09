from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse as api_reverse
from django.test import TestCase
from django.contrib.auth.models import User
from faker import Factory
from rest_framework import status

faker = Factory.create()
profile = faker.profile(fields=None, sex=None)
register_api = api_reverse('auth_api:api-register')
login_api = api_reverse('auth_api:login')
password = faker.password()


class UserAPITestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username=profile['username'], email=profile['mail'])
        user.set_password(password)
        user.save()

    def test_created_user_std(self):
        qs = User.objects.filter(username=profile['username'])
        self.assertEqual(qs.count(), 1)

    def test_register_user_api_fail(self):
        url = register_api
        password = faker.password()
        data = {
            "username": profile['username'],
            "password": password,
            "password2": password,
            "email": profile['mail']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_api(self):
        url = register_api
        profile_ = faker.profile(fields=None, sex=None)
        password = faker.password()
        data = {
            "username": profile_['username'],
            "password": password,
            "password2": password,
            "email": profile_['mail']
        }
        response = self.client.post(url, data, format='json')
        token_len = len(response.data.get('token', 0))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(token_len, 1, 'token not found')

    def test_login_user_api_username(self):
        url = login_api
        data = {
            "username": profile['username'],
            "password": password,
        }
        response = self.client.post(url, data, format='json')
        token_len = len(response.data.get('token', 0))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(token_len, 1, 'token not found')
        token = response.data.get('token', None)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response2 = client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_user_api_email(self):
        url = login_api
        data = {
            "username": profile['mail'],
            "password": password,
        }
        response = self.client.post(url, data, format='json')
        token_len = len(response.data.get('token', 0))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(token_len, 1, 'token not found')

    def test_login_user_api_fail(self):
        url = login_api
        data = {
            "username": profile['mail'],
            "password": '123',
        }
        response = self.client.post(url, data, format='json')
        token = response.data.get('token', None)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(token, None, 'token  found')
