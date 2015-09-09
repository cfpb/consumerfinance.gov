from .base import *
import v1

GRUNT_WATCH = [SITE_ROOT]

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

SHEER_SITES = [os.path.dirname(v1.__file__) + '/jinja2/v1']
SHEER_ELASTICSEARCH_SERVER = 'localhost:9200'
SHEER_ELASTICSEARCH_INDEX = 'content'

INSTALLED_APPS += ('django_extensions',)
