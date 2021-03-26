from django.contrib.auth.models import User
from django.test import TestCase


class LoginViewsTestCase(TestCase):

    def test_login_with_lockout_no_auth(self):
        response = self.client.get('/login/?next=https://example.com')
        self.assertTemplateUsed(response, 'wagtailadmin/login.html')
        self.assertEqual(response.context['next'], '/admin/')

    def test_login_with_lockout_failed_login(self):
        self.client.post(
            '/login/',
            {'username': 'admin', 'password': 'badadmin'}
        )
        self.assertIsNotNone(
            User.objects.get(username='admin').failedloginattempt
        )

    def test_login_with_lockout_success_after_failed_login(self):
        response = self.client.post(
            '/login/',
            {'username': 'admin', 'password': 'badadmin'}
        )
        response = self.client.post(
            '/login/',
            {'username': 'admin', 'password': 'admin'}
        )
        self.assertRedirects(
            response,
            '/login/check_permissions/?next=/admin/',
            target_status_code=302,
            fetch_redirect_response=False,
        )

    def test_login_with_lockout_success(self):
        response = self.client.post(
            '/login/',
            {'username': 'admin', 'password': 'admin'}
        )
        self.assertRedirects(
            response,
            '/login/check_permissions/?next=/admin/',
            target_status_code=302,
            fetch_redirect_response=False,
        )

    def test_login_with_lockout_authenticated_redirects(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/login/')
        self.assertRedirects(
            response,
            '/login/check_permissions/?next=/admin/',
            target_status_code=302,
            fetch_redirect_response=False,
        )

    def test_check_permissions_no_auth(self):
        response = self.client.get('/login/check_permissions/?next=/admin/')
        self.assertRedirects(response, '/login/?next=/admin/')

    def test_check_permissions_next_url_does_not_exist(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/login/check_permissions/?next=/badurl/')
        self.assertRedirects(response, '/admin/')

    def test_check_permissions_next_url_unsafe(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(
            '/login/check_permissions/?next=https://google.com/'
        )
        self.assertRedirects(response, '/admin/')

    def test_check_permissions_next_permissions_problem(self):
        User.objects.create_user(
            username='noperm', email='', password='noperm'
        )
        self.client.login(username='noperm', password='noperm')
        response = self.client.get('/login/check_permissions/?next=/admin/')
        self.assertIn(
            b'You do not have permission to access this page.',
            response.content
        )
