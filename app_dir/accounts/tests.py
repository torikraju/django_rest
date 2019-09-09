from django.test import TestCase
from django.contrib.auth.models import User
from faker import Factory

faker = Factory.create()
profile = faker.profile(fields=None, sex=None)


class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=profile['username'], email=profile['mail'])
        user.set_password('1')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username=profile['username'])
        self.assertEqual(qs.count(), 1)
