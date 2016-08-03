from v1.models.home_page import HomePage
from django.contrib.auth.models import User


def save_page(child, root=None):
	if not root:
		root = HomePage.objects.get(title='CFGOV')
	admin_user = User.objects.get(username='admin')

	root.add_child(instance = child)
	return child.save_revision(
		user=admin_user,
		submitted_for_moderation=False,
	)

def publish_page(child, root=None):
	revision = save_page(child=child)
	revision.publish()

