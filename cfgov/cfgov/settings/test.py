from .local import *

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
