from django.test import RequestFactory, TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()


class TestUserPermissionsView(TestCase):
    def setUp(self):
        self.testuser = User.objects.create_superuser(username='foo',
                                                      password='bar', email='foo@cfpb.gov')
        self.testuser.save()

    def test_user_has_page(self):
        client = Client()
        login_response = client.login(username='foo', password='bar')
        url = reverse('permissions:user', args=[self.testuser.pk])

        response = client.get(url)

        import pdb
        pdb.set_trace()
        self.assertEqual(response.status_code, 200)
