from unipath import DIRS

from .base import *
from .production import STATICFILES_STORAGE, STATIC_ROOT


# STATICFILES_DIRS += [str(d) for d in REPOSITORY_ROOT.child('static.in').listdir(filter=DIRS)]
