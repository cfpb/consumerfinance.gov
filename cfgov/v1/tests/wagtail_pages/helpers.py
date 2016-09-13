from django.contrib.auth.models import User

from v1.models.home_page import HomePage


def save_page(page):
    admin_user = User.objects.get(username='admin')
    page.save()
    return page.save_revision(user=admin_user)


def save_new_page(child, root=None):
    if not root:
        root = HomePage.objects.get(title='CFGov')
    root.add_child(instance=child)
    return save_page(page=child)


def publish_page(child):
    revision = save_new_page(child=child)
    revision.publish()
