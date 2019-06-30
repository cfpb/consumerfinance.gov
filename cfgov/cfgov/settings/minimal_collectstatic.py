import warnings

from unipath import Path, DIRS

from .base import *
from .production import STATICFILES_STORAGE

if Path.cwd().child('static.in').exists():
    STATICFILES_DIRS += [str(d) for d in Path.cwd().child('static.in').listdir(filter=DIRS)]
