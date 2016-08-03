from v1.models.home_page import HomePage
from django.contrib.auth.models import User


def publish_page(child, root=None):
	if not root:
		root = HomePage.objects.get(title='CFGOV')
	admin_user = User.objects.get(username='admin')

	root.add_child(instance = child)
	revision = child.save_revision(
		user=admin_user,
		submitted_for_moderation=False,
	)
	revision.publish()

