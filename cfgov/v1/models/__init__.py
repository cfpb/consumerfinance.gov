from django.conf import settings
from .base import *
from .events import *
from .molecules import *
from .organisms import *
from .snippets import *
from .landing_page import *
from .ref import *

if settings.DEBUG:
    from .demo import *
