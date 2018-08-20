from collections import defaultdict

import django

from core.utils import NoMigrations

from .test import *


if django.VERSION[:2] < (1, 9):
    MIGRATION_MODULES = NoMigrations()
else:
    MIGRATION_MODULES = defaultdict(None)
