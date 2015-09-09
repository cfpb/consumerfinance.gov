import os
import subprocess
import atexit
import signal

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command\
    as StaticfilesRunserverCommand


# Inspired by:
# https://lincolnloop.com/blog/simplifying-your-django-frontend-tasks-grunt/
# Extended to potentially support multiple grunt-watched directories.

class Command(StaticfilesRunserverCommand):

    def inner_run(self, *args, **options):
        self.start_grunt()
        return super(Command, self).inner_run(*args, **options)

    def start_grunt(self):
        self.grunt_processes = []
        for dir in settings.GRUNT_WATCH:
            self.stdout.write('>>> Starting grunt in %s' % dir)
            sub = subprocess.Popen(
                'grunt watch',
                shell=True,
                stdin=subprocess.PIPE,
                stdout=self.stdout,
                stderr=self.stderr,
                cwd = settings.CFGOV_REFRESH,
            )

            self.grunt_processes.append(sub)

            self.stdout.write('>>> Grunt process on pid {0}'.format(sub.pid))

        def kill_grunt_processes(processes):
            for process in processes: 
                self.stdout.write('>>> Closing grunt process %s' % process.pid)
                os.kill(process.pid, signal.SIGTERM)

        atexit.register(kill_grunt_processes, self.grunt_processes)
