import os

import dj_database_url


DATABASES = {}
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config()
else:
    DATABASES['default'] =  {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_NAME', ''),
        'USER': os.environ.get('MYSQL_USER', ''),
        'PASSWORD': os.environ.get('MYSQL_PW', ''),
        'HOST': os.environ.get('MYSQL_HOST', ''),
        'PORT': os.environ.get('MYSQL_PORT', ''),
    }

# Allow us to configure the default MySQL storage engine via the environment.
if 'STORAGE_ENGINE' in os.environ:
    db_options = {
        'init_command': os.environ['STORAGE_ENGINE'],
    }

    for db_label in DATABASES.keys():
        DATABASES[db_label]['OPTIONS'] = db_options

if 'PG_DATABASE_URL' in os.environ:
    DATABASES['postgres'] = dj_database_url.config('PG_DATABASE_URL')
