from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class ESHealthTestCase(TestCase):
    def test_bad_connection_name(self):
        with self.assertRaises(CommandError):
            call_command("es_health", "notarealconnection", stdout=StringIO())

    @mock.patch("elasticsearch_dsl.connections.get_connection")
    def test_foo(self, mock_es_get_connection):
        mock_elasticsearch = mock.MagicMock()
        mock_elasticsearch.cat.health.return_value = "health table"
        mock_elasticsearch.cat.indices.return_value = "indices table"
        mock_elasticsearch.cat.aliases.return_value = "aliases table"
        mock_es_get_connection.return_value = mock_elasticsearch

        out = StringIO()
        call_command("es_health", stdout=out, stderr=out)
        self.assertIn("Health:\nhealth table", out.getvalue())
        self.assertIn("Indices:\nindices table", out.getvalue())
        self.assertIn("Aliases:\naliases table", out.getvalue())
