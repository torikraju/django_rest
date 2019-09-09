from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse as api_reverse
from django.test import TestCase
from django.contrib.auth.models import User
from faker import Factory
from rest_framework import status
from app_dir.status.models import Status

faker = Factory.create()
profile = faker.profile(fields=None, sex=None)
register_api = api_reverse('auth_api:api-register')
login_api = api_reverse('auth_api:login')
create_api = api_reverse('status_api:status-creator')
password = faker.password()
login_data = {
    "username": profile['mail'],
    "password": password,
}


def rud_api(id_):
    return api_reverse('status_api:status-details', kwargs={'pk': id_})


content_data = {
    'content': faker.sentence(nb_words=20, variable_nb_words=True, ext_word_list=None)
}


class StatusAPITestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username=profile['username'], email=profile['mail'])
        user.set_password(password)
        user.save()
        Status.objects.create(
            user=user,
            content=faker.paragraphs(nb=3, ext_word_list=None)
        )

    def test_statuses(self):
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)

    def get_token(self):
        url = login_api
        response = self.client.post(url, login_data, format='json')
        return response.data.get('token', None)

    def test_status_crud(self):
        token = self.get_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        create = client.post(create_api, content_data, format='json')
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 2)
        id_ = create.data.get('id')
        '''update'''
        update = client.put(rud_api(id_), content_data, format='json')
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        '''get'''
        get = client.get(rud_api(id_), format='json')
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        '''delete'''
        delete = client.delete(rud_api(id_), format='json')
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_status_no_token_create(self):
        client = APIClient()
        response = client.post(create_api, content_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_status_rud_no_token(self):
        client = APIClient()
        token = self.get_token()
        client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        create = client.post(create_api, content_data, format='json')
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        id_ = create.data.get('id')
        client.credentials(HTTP_AUTHORIZATION='')
        '''update'''
        update = client.put(rud_api(id_), content_data, format='json')
        self.assertEqual(update.status_code, status.HTTP_401_UNAUTHORIZED)
        '''get'''
        get = client.get(rud_api(id_), format='json')
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        '''delete'''
        delete = client.delete(rud_api(id_), format='json')
        self.assertEqual(delete.status_code, status.HTTP_401_UNAUTHORIZED)
