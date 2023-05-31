from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserSaveTestCase(TestCase):
    def make_user(self, password):
        return User.objects.create_user(username="testuser", password=password)

    def test_user_create_makes_history_item(self):
        user = self.make_user(password="foo")
        phi = user.password_history.latest()

        self.assertEqual(user.password, phi.encrypted_password)

    def test_user_save_new_password_makes_history_item(self):
        user = self.make_user(password="foo")
        first_phi = user.password_history.latest()

        user.set_password("bar")
        user.save()
        new_phi = user.password_history.latest()

        self.assertNotEqual(first_phi, new_phi)
        self.assertEqual(user.password, new_phi.encrypted_password)

    def test_user_save_same_password_no_history_item(self):
        user = self.make_user(password="foo")
        first_phi = user.password_history.latest()

        user.save()
        new_phi = user.password_history.latest()

        self.assertEqual(first_phi, new_phi)
        self.assertEqual(user.password, new_phi.encrypted_password)
