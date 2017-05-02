from django.contrib.auth.models import User

def run():
	try:
		User.objects.get(username='test')
	except User.DoesNotExist:
		User.objects.create_superuser(
		         	username='test',
		            email='test@email.com',
		            password='password'
		        )
