from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    """
    convert all tables to innodb
    unchanged from solution proposed at 
    https://stackoverflow.com/a/15389961/104365
    """

    def handle(self, database="default", *args, **options):

        cursor = connections[database].cursor()

        cursor.execute("SHOW TABLE STATUS")

        for row in cursor.fetchall():
            if row[1] == "MyISAM":
                print "Converting %s" % row[0],
                print cursor.execute("ALTER TABLE %s ENGINE=INNODB" % row[0])
