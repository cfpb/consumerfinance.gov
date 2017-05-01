from django.contrib.auth.models import User

def run():
	User.objects.create_superuser(
	         	username='test',
	            email='test@email.com',
	            password='password'
	        )