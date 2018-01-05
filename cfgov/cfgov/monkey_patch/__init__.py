from __future__ import absolute_import

from django import VERSION
from django.db.migrations import executor, migration

from cfgov.monkey_patch.django import Django19MigrationExecutor


# Monkeypatch Django 1.8 migration executor to use the much faster version
# from Django 1.9.1.
if VERSION[:2] < (1, 9):
    executor.MigrationExecutor = Django19MigrationExecutor
    migration.Migration.initial = None
