from cfgov.settings.base import *

# Repository root is 4 levels above this file
REPOSITORY_ROOT = Path(__file__).ancestor(4)

# This is the root of the Django project, 'cfgov'
PROJECT_ROOT = REPOSITORY_ROOT.child('cfgov')
V1_TEMPLATE_ROOT = PROJECT_ROOT.child('jinja2', 'v1')

DEBUG = True

SECRET_KEY = 'not-secret-key-for-testing'

INSTALLED_APPS += (
    'sslserver',
    'wagtail.contrib.wagtailstyleguide',
)
MEDIA_ROOT = os.environ.get('MEDIA_ROOT',
                            os.path.join(PROJECT_ROOT, 'f'))

if not COLLECTSTATIC:
    if os.environ.get('DATABASE_ROUTING', False):
        DATABASE_ROUTERS = ['v1.db_router.CFGOVRouter', 'v1.db_router.LegacyRouter']

        DATABASES = {
            'default': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('MYSQL_NAME', ''),
                'USER': os.environ.get('MYSQL_USER', ''),
                'PASSWORD': os.environ.get('MYSQL_PW', ''),
                'HOST': os.environ.get('MYSQL_HOST', ''),
                'PORT': os.environ.get('MYSQL_PORT', ''),
                'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET storage_engine=MYISAM') },
            },
            'legacy': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('LEGACY_MYSQL_NAME', ''),
                'USER': os.environ.get('LEGACY_MYSQL_USER', ''),
                'PASSWORD': os.environ.get('LEGACY_MYSQL_PW', ''),
                'HOST': os.environ.get('LEGACY_MYSQL_HOST', ''),
                'PORT': os.environ.get('LEGACY_MYSQL_PORT', ''),
                'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET storage_engine=MYISAM') },
            },
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': MYSQL_ENGINE,
                'NAME': os.environ.get('MYSQL_NAME', ''),
                'USER': os.environ.get('MYSQL_USER', ''),
                'PASSWORD': os.environ.get('MYSQL_PW', ''),
                'HOST': os.environ.get('MYSQL_HOST', ''),
                'PORT': os.environ.get('MYSQL_PORT', ''),
                'OPTIONS': {'init_command': os.environ.get('STORAGE_ENGINE', 'SET storage_engine=MYISAM') },
            },
        }

STATIC_ROOT = REPOSITORY_ROOT.child('collectstatic')

ALLOW_ADMIN_URL = DEBUG or os.environ.get('ALLOW_ADMIN_URL', False)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}


MIDDLEWARE_CLASSES += CSP_MIDDLEWARE_CLASSES
CSP_REPORT_ONLY = True


PICARD_SCRIPTS_DIRECTORY = os.environ.get('PICARD_SCRIPTS_DIRECTORY',REPOSITORY_ROOT.child('picard_scripts'))

SHEER_SITES = {
        'assets': V1_TEMPLATE_ROOT,
        'owning-a-home':
            Path(os.environ.get('OAH_SHEER_PATH') or
            Path(REPOSITORY_ROOT, '../owning-a-home/dist')),
        'fin-ed-resources':
            Path(os.environ.get('FIN_ED_SHEER_PATH') or
            Path(REPOSITORY_ROOT, '../fin-ed-resources/dist')),
        'know-before-you-owe':
            Path(os.environ.get('KBYO_SHEER_PATH') or
            Path(REPOSITORY_ROOT, '../know-before-you-owe/dist')),
}

