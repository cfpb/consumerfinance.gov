from subprocess import call
from django.conf import settings

from django.core.management.base import CommandError
from django.core.management.commands import dbshell


class Command(dbshell.Command):
    def handle(self, **options):
        try:
            # try the default behavior first
            super(Command, self).handle(**options)
        except CommandError:
            # if that didn't work, try docker-compose
            call(['docker-compose', 'exec', 'mysql', 'mysql', 'v1', '-u',
                  'root', '-proot'], cwd=settings.REPOSITORY_ROOT)
