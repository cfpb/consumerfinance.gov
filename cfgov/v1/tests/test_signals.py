from unittest import TestCase

from django.contrib.auth.models import User
from django.utils import timezone

from model_bakery import baker


class UserSaveTestCase(TestCase):
    def make_user(self, password, is_superuser=False):
        user = baker.prepare(User, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def test_user_save_new_password_makes_history_item(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()

        user.set_password('bar')
        user.save()
        new_phi = user.passwordhistoryitem_set.latest()

        self.assertNotEqual(first_phi, new_phi)
        self.assertEqual(user.password, new_phi.encrypted_password)

    def test_user_save_new_password_not_expired(self):
        user = self.make_user(password='foo')
        user.set_password('bar')
        user.save()

        new_phi = user.passwordhistoryitem_set.latest()
        self.assertGreater(new_phi.expires_at, timezone.now())

    def test_user_save_new_password_locks_password(self):
        user = self.make_user(password='foo')
        user.set_password('bar')
        user.save()

        new_phi = user.passwordhistoryitem_set.latest()
        self.assertGreater(new_phi.locked_until, timezone.now())

    def test_user_save_same_password_no_history_item(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()

        user.save()
        new_phi = user.passwordhistoryitem_set.latest()

        self.assertEqual(first_phi, new_phi)
        self.assertEqual(user.password, new_phi.encrypted_password)

    def test_user_created_expires_password(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertLess(first_phi.expires_at, timezone.now())

    def test_user_created_unlocks_password(self):
        user = self.make_user(password='foo')
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertLess(first_phi.locked_until, timezone.now())

    def test_superuser_created_does_not_expire_password(self):
        user = self.make_user(password='foo', is_superuser=True)
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertGreater(first_phi.expires_at, timezone.now())

    def test_superuser_created_unlocks_password(self):
        user = self.make_user(password='foo', is_superuser=True)
        first_phi = user.passwordhistoryitem_set.latest()
        self.assertLess(first_phi.locked_until, timezone.now())
