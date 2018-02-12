from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

User = get_user_model()


class TestPermissionsViews(TestCase):
    def setUp(self):
        self.testuser = User.objects.create_superuser(
            username='foo',
            password='bar',
            email='foo@cfpb.gov')
        self.testuser.save()

        self.testgroup = Group.objects.create(name='Developers')
        self.testgroup.user_set.add(self.testuser)

    def test_user_has_page(self):
        client = Client()
        client.login(username='foo', password='bar')
        url = reverse('permissions:user', args=[self.testuser.pk])

        response = client.get(url)

        self.assertContains(response, 'Developers')

    def test_user_on_group_page(self):
        client = Client()
        client.login(username='foo', password='bar')

        url = reverse('permissions:group', args=[self.testgroup.pk])

        response = client.get(url)

        self.assertContains(response, 'foo')
