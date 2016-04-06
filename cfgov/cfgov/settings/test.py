from .local import *

if os.environ.get('TRAVIS_SETTING'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
        }
    }