from django.test import TestCase

from models.users.models import User
from models.users.tests.factories import UserFactory, TEST_PWD


class UserModelTestCase(TestCase):
    def test__create(self):
        create_kwargs = dict(username="test", email="myemail@test.com", password="test")
        instance = User.objects.create_user(**create_kwargs)
        self.assertIsNotNone(instance.id)
        self.assertEqual(instance.username, create_kwargs["username"])
        self.assertEqual(instance.email, create_kwargs["email"])
        self.assertTrue(instance.check_password(create_kwargs["password"]))

    def test__factory(self):
        instance = UserFactory()
        instance.refresh_from_db()
        self.assertIsNotNone(instance.id)
        self.assertIsInstance(instance.username, str)
        self.assertIsInstance(instance.email, str)
        self.assertTrue(instance.check_password(TEST_PWD))
