from .local import *

if not os.environ.get('TRAVIS_SETTING'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'testdb',
            'USER': os.environ.get('MYSQL_USER'),
            'PASSWORD': os.environ.get('MYSQL_PW', ''),
            'HOST': os.environ.get('MYSQL_HOST', ''),  # empty string == localhost
            'PORT': os.environ.get('MYSQL_PORT', ''),  # empty string == default
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
        }
    }