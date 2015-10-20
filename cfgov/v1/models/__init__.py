from django.conf import settings
from .base import *
from .events import *
from .molecules import *
from .organisms import *
if settings.DEBUG :
    from .demo import *
