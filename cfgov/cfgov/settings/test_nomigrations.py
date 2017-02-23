from .test import *


class NoMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'nomigrations'

MIGRATION_MODULES = NoMigrations()
