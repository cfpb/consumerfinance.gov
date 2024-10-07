from django.apps import apps
from django.test import TestCase

from wagtail.users.wagtail_hooks import get_viewset_cls

from login.forms import UserCreationForm, UserEditForm


class UserViewSetTestCase(TestCase):
    """Test that the wagtailusers app config loads our UserViewSet.

    This tests both our UserViewSet class (which just returns our custom forms)
    as well as our LoginUsersAppConfig in apps.py.
    """

    def test_get_form_class_edit(self):
        app_config = apps.get_app_config("wagtailusers")
        user_viewset_cls = get_viewset_cls(app_config, "user_viewset")
        viewset = user_viewset_cls(name="wagtailusers_users")
        form_class = viewset.get_form_class(for_update=True)
        self.assertEqual(form_class, UserEditForm)

    def test_get_form_class_create(self):
        app_config = apps.get_app_config("wagtailusers")
        user_viewset_cls = get_viewset_cls(app_config, "user_viewset")
        viewset = user_viewset_cls(name="wagtailusers_users")
        form_class = viewset.get_form_class()
        self.assertEqual(form_class, UserCreationForm)
