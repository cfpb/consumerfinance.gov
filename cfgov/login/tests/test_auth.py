from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, override_settings
from django.test.client import RequestFactory

from login.auth import (
    CFPBOIDCAuthenticationBackend,
    ensure_wagtail_users_group_membership,
    process_family_name_claim,
    process_given_name_claim,
    process_roles_admin,
    process_roles_claim,
    username_from_email,
)


User = get_user_model()


class UsernameFromEmailTestCase(TestCase):
    def test_email_address(self):
        self.assertEqual(username_from_email("test@example.com"), "test")


class ProcessRolesClaimTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="user1", email="email@example.com", first_name="User"
        )
        self.group = Group.objects.get(name="Wagtail Users")
        self.admin_permission = Permission.objects.get(
            codename="access_admin",
            content_type=ContentType.objects.get(
                app_label="wagtailadmin", model="admin"
            ),
        )
        self.group.permissions.add(self.admin_permission)

    @patch("login.auth.ensure_wagtail_users_group_membership")
    @patch("login.auth.process_roles_admin")
    def test_process_roles_claim(
        self,
        mock_process_roles_admin,
        mock_ensure_wagtail_users_group_membership,
    ):
        mock_process_roles_admin.side_effect = [True, False, None]

        result = process_roles_claim(
            self.user,
            [
                "admin-role",
            ],
        )
        self.assertTrue(result)
        result = process_roles_claim(
            self.user,
            [
                "admin-role",
            ],
        )
        self.assertFalse(result)
        result = process_roles_claim(
            self.user,
            [
                "admin-role",
            ],
        )
        self.assertFalse(result)

    @override_settings(OIDC_OP_ADMIN_ROLE=None)
    def test_process_roles_admin_skip(self):
        result = process_roles_admin(self.user, [])
        self.assertIsNone(result)

    @override_settings(OIDC_OP_ADMIN_ROLE="admin-user")
    def test_process_roles_admin_adds_superuser(self):
        result = process_roles_admin(self.user, ["admin-user"])
        self.assertTrue(result)
        self.assertTrue(self.user.is_superuser)

    @override_settings(OIDC_OP_ADMIN_ROLE="admin-user")
    def test_process_roles_admin_removes_superuser(self):
        self.user.is_superuser = True
        result = process_roles_admin(self.user, [])
        self.assertTrue(result)
        self.assertFalse(self.user.is_superuser)

    @override_settings(OIDC_OP_ADMIN_ROLE="admin-user")
    def test_process_roles_admin_preserves_superuser(self):
        self.user.is_superuser = True
        result = process_roles_admin(self.user, ["admin-user"])
        self.assertFalse(result)
        self.assertTrue(self.user.is_superuser)

    def test_ensure_wagtail_users_group_membership_group_does_not_exist(self):
        Group.objects.get(name="Wagtail Users").delete()

        with self.assertRaises(Group.DoesNotExist):
            Group.objects.get(name="Wagtail Users")

        result = ensure_wagtail_users_group_membership(self.user)
        self.assertIsNone(result)

    def test_process_roles_user_adds_group(self):
        ensure_wagtail_users_group_membership(self.user)
        self.assertTrue(self.user.has_perm("wagtailadmin.access_admin"))

    def test_process_roles_user_preserves_group(self):
        self.user.groups.add(self.group)
        ensure_wagtail_users_group_membership(self.user)
        self.assertTrue(self.user.has_perm("wagtailadmin.access_admin"))

    def test_process_given_name_claim(self):
        result = process_given_name_claim(self.user, "Test")
        self.assertTrue(result)
        self.assertEqual(self.user.first_name, "Test")

    def test_process_family_name_claim(self):
        result = process_family_name_claim(self.user, "User")
        self.assertTrue(result)
        self.assertEqual(self.user.last_name, "User")


class CFPBOIDCAuthenticationBackendTestCase(TestCase):
    @override_settings(
        OIDC_OP_TOKEN_ENDPOINT="https://server.example.com/token"
    )
    @override_settings(OIDC_OP_USER_ENDPOINT="https://server.example.com/user")
    @override_settings(OIDC_RP_CLIENT_ID="example_id")
    @override_settings(OIDC_RP_CLIENT_SECRET="client_secret")
    def setUp(self):
        self.backend = CFPBOIDCAuthenticationBackend()
        self.user = User.objects.create(
            username="user1", email="email@example.com", first_name="User"
        )

        # To check any django.contrib.messages applied to a request by our
        # auth backend, we need a request, and that request needs session and
        # message storage, so we run it through those middlewares.
        self.factory = RequestFactory()
        self.backend.request = self.factory.get("/admin")
        session_middleware = SessionMiddleware(get_response=lambda r: r)
        session_middleware.process_request(self.backend.request)
        self.backend.request.session.save()
        message_middleware = MessageMiddleware(get_response=lambda r: r)
        message_middleware.process_request(self.backend.request)
        self.backend.request.session.save()

    @patch("mozilla_django_oidc.auth.OIDCAuthenticationBackend.get_userinfo")
    def test_get_userinfo_preserves_roles(self, mock_get_userinfo):
        mock_get_userinfo.return_value = {
            "email": "test@example.com",
        }
        payload_with_roles = {
            "email": "test@example.com",
            "roles": [
                "admin-user",
                "regular-user",
                "something-else",
            ],
        }
        claims = self.backend.get_userinfo(
            "access_token", "id_token", payload_with_roles
        )
        self.assertIn("roles", claims)
        self.assertEqual(len(claims["roles"]), 3)

    @override_settings(
        OIDC_CLAIMS_PROCESSORS={
            "given_name": "login.auth.process_given_name_claim",
            "unavailable_claim": lambda u, c: True,
        }
    )
    def test_process_claims(self):
        resulting_user = self.backend.process_claims(
            self.user, {"given_name": "Test", "unprocessed_claim": True}
        )
        self.assertEqual(resulting_user.first_name, "Test")

    @patch("login.auth.CFPBOIDCAuthenticationBackend.process_claims")
    def test_update_user(self, mock_process_claims):
        self.backend.update_user(self.user, {})
        # Our modification to update_user is to add a call to process_claims.
        # Ensure that happens.
        self.assertTrue(mock_process_claims.called)

    @patch("login.auth.CFPBOIDCAuthenticationBackend.process_claims")
    def test_create_user(self, mock_process_claims):
        self.backend.create_user({"email": "test@example.com"})
        # Our modification to create_user is to ultimately call process_claims.
        # Ensure that happens.
        self.assertTrue(mock_process_claims.called)

    @override_settings(OIDC_USERNAME_ALGO="login.auth.username_from_email")
    def test_create_user_already_exists(self):
        User.objects.create(username="test")
        result = self.backend.create_user({"email": "test@example.com"})
        self.assertIsNone(result)
        messages = list(get_messages(self.backend.request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message,
            "There was an error creating a user for test@example.com",
        )
