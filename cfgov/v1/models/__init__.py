from django.conf import settings
from .base import *
from .events import *
from .atoms import *
from .molecules import *
from .organisms import *
from .snippets import *
from .landing_page import *
from .sublanding_page import *
from .browse_page import *
from .learn_page import *
from .doc_detail_page import *
from .ref import *

if settings.DEBUG:
    from .demo import *
