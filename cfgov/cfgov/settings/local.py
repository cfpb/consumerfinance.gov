from .base import *

GRUNT_WATCH = [CFGOV_REFRESH]

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

SHEER_SITES = [CFGOV_REFRESH.child('dist')]
SHEER_ELASTICSEARCH_SERVER = 'localhost:9200'
SHEER_ELASTICSEARCH_INDEX = 'content'

INSTALLED_APPS += ('django_extensions',)
