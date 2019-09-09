from django.test import TestCase
from django.contrib.auth.models import User
from faker import Factory

from .models import Status

faker = Factory.create()
profile = faker.profile(fields=None, sex=None)


class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=profile['username'], email=profile['mail'])
        user.set_password('1')
        user.save()

    def test_created_status(self):
        user = User.objects.get(username=profile['username'])
        status = Status.objects.create(
            user=user,
            content=faker.paragraphs(nb=3, ext_word_list=None)
        )
        self.assertEqual(status.user, user)
        qs = Status.objects.all()
        self.assertGreaterEqual(qs.count(), 1)
