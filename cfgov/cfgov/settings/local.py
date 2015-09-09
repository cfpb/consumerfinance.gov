from .base import *
import v1

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

SHEER_SITES = [os.path.dirname(v1.__file__) + '/jinja2/v1']
SHEER_ELASTICSEARCH_SERVER = os.environ.get('ES_HOST') + ':' + os.environ.get('ES_PORT')
SHEER_ELASTICSEARCH_INDEX = os.environ.get('SHEER_ELASTICSEARCH_INDEX')

INSTALLED_APPS += ('django_extensions',)
