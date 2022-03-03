from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestPermissionsViews(TestCase):
    def setUp(self):
        self.testuser = User.objects.create_superuser(
            username="foo", password="bar", email="foo@cfpb.gov"
        )
        self.testuser.save()

        self.testgroup = Group.objects.create(name="Developers")
        self.testgroup.user_set.add(self.testuser)

    def test_user_has_page(self):
        self.client.login(username="foo", password="bar")
        url = reverse("permissions:user", args=[self.testuser.pk])

        response = self.client.get(url)

        self.assertContains(response, "Developers")

    def test_user_on_group_page(self):
        self.client.login(username="foo", password="bar")

        url = reverse("permissions:group", args=[self.testgroup.pk])

        response = self.client.get(url)

        self.assertContains(response, "foo")

    def test_user_and_group_on_index_page(self):
        self.client.login(username="foo", password="bar")

        url = reverse("permissions:index")

        response = self.client.get(url)

        self.assertContains(response, "foo")
        self.assertContains(response, "Developers")

    def group_model_permission(self):
        self.client.login(username="foo", password="bar")

        testpermission = Permission.objects.get(name="Can add log entry")
        self.testgroup.permissions.add(testpermission)

        url = reverse("permissions:user", args=[self.testuser.pk])
        response = self.client.get(url)

        self.assertContains(response, "Can add log entry")
