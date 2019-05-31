import warnings

from unipath import DIRS

from .base import *

STATIC_ROOT = REPOSITORY_ROOT.child('collectstatic')
STATICFILES_DIRS += [str(d) for d in REPOSITORY_ROOT.child('static.in').listdir(filter=DIRS)]
