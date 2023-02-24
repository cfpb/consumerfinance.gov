from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.timezone import now

from wagtail.tests.utils import WagtailTestUtils

from login.models import TemporaryLockout
from login.views import CFGOVPasswordResetConfirmView


class PasswordResetViewTestCase(TestCase, WagtailTestUtils):
    # The setup methods come from Wagtail's TestPasswordReset test case.
    # They handle user and password-reset token creation.
    def setUp(self):
        # Create a user
        self.create_superuser(
            username="test", email="test@email.com", password="password"
        )

    def setup_password_reset_confirm_tests(self):
        # Get user
        self.user = get_user_model().objects.get(email="test@email.com")

        # Generate a password reset token
        self.password_reset_token = PasswordResetTokenGenerator().make_token(
            self.user
        )

        # Generate a password reset uid
        self.password_reset_uid = force_str(
            urlsafe_base64_encode(force_bytes(self.user.pk))
        )

        # Create url_args
        token = CFGOVPasswordResetConfirmView.reset_url_token

        self.url_kwargs = dict(uidb64=self.password_reset_uid, token=token)

        # Add token to session object
        s = self.client.session
        s.update(
            {
                auth_views.INTERNAL_RESET_SESSION_TOKEN: self.password_reset_token,
            }
        )
        s.save()

    def test_password_reset_confirm_view_post_password_invalid(self):
        """
        Test that the password is invalid because it fails one of our custom
        password validators. This ensures our subclass of Wagtail's password
        reset confirmation view is using our password form.
        """
        self.setup_password_reset_confirm_tests()

        # Post new password to change password page
        post_data = {
            "new_password1": "eleven",
            "new_password2": "eleven",
        }
        response = self.client.post(
            reverse(
                "wagtailadmin_password_reset_confirm", kwargs=self.url_kwargs
            ),
            post_data,
        )

        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(response.context_data["form"].is_valid())

    def test_password_reset_confirm_view_post_removes_lockout(self):
        """
        Test that resetting the password successfully removes a temporary
        lockout.
        """

        self.setup_password_reset_confirm_tests()

        TemporaryLockout(user=self.user, expires_at=now() + timedelta(hours=1))

        # Post new password to change password page
        post_data = {
            "new_password1": "GoodPassword1!",
            "new_password2": "GoodPassword1!",
        }
        response = self.client.post(
            reverse(
                "wagtailadmin_password_reset_confirm", kwargs=self.url_kwargs
            ),
            post_data,
        )

        self.assertRedirects(
            response, reverse("wagtailadmin_password_reset_complete")
        )

        updated_user = get_user_model().objects.get(email="test@email.com")

        self.assertTrue(updated_user.check_password("GoodPassword1!"))
        self.assertEqual(len(updated_user.temporarylockout_set.all()), 0)
