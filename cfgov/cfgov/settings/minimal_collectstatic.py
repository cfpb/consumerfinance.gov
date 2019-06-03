import warnings

from unipath import DIRS

from .base import *
from .production import STATICFILES_STORAGE


STATICFILES_DIRS += [str(d) for d in REPOSITORY_ROOT.child('static.in').listdir(filter=DIRS)]
