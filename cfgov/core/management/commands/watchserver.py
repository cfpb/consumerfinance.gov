import atexit
import os
import signal
import subprocess

from django.contrib.staticfiles.management.commands.runserver import \
    Command as StaticfilesRunserverCommand


# Inspired by:
# https://lincolnloop.com/blog/simplifying-your-django-frontend-tasks-grunt/

class Command(StaticfilesRunserverCommand):

    def inner_run(self, *args, **options):
        self.start_gulp()
        return super(Command, self).inner_run(*args, **options)

    def start_gulp(self):
        self.stdout.write('>>> Starting gulp in %s' % dir)
        sub = subprocess.Popen(
            'gulp watch',
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.gulp_process = sub

        self.stdout.write('>>> Gulp process on pid {0}'.format(sub.pid))

        def kill_gulp_process(sub):
            self.stdout.write('>>> Closing gulp process %s' % sub.pid)
            os.kill(sub.pid, signal.SIGTERM)

        atexit.register(kill_gulp_process, self.gulp_process)
