from django.core.management.base import BaseCommand, CommandError

from elasticsearch_dsl import connections


class Command(BaseCommand):
    help = "Report the health of configued Elasticsearch clusters and indices"

    def add_arguments(self, parser):
        parser.add_argument(
            "connection",
            nargs="?",
            default="default",
            help="The name of the Elasticsearch connection from settings",
        )

    def handle(self, *args, **options):
        try:
            es = connections.get_connection(options["connection"])
        except KeyError:
            raise CommandError(
                "Couldn't get an Elasticsearch connection named "
                f"{options['connection']}"
            )

        health = es.cat.health(v=True)
        self.stdout.write(f"Health:\n{health}\n")

        indices = es.cat.indices(v=True)
        self.stdout.write(f"Indices:\n{indices}\n")

        aliases = es.cat.aliases(v=True)
        self.stdout.write(f"Aliases:\n{aliases}")
