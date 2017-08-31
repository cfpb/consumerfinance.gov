import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_NAME', ''),
        'USER': os.environ.get('MYSQL_USER', ''),
        'PASSWORD': os.environ.get('MYSQL_PW', ''),
        'HOST': os.environ.get('MYSQL_HOST', ''),
        'PORT': os.environ.get('MYSQL_PORT', ''),
    },
}

# Allow us to configure the default MySQL storage engine via the environment.
if 'STORAGE_ENGINE' in os.environ:
    db_options = {
        'init_command': os.environ['STORAGE_ENGINE'],
    }

    for db_label in DATABASES.keys():
        DATABASES[db_label]['OPTIONS'] = db_options
