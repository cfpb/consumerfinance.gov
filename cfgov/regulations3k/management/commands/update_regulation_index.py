from __future__ import unicode_literals

import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

from regulations3k.models import Part, Section


logger = logging.getLogger(__name__)


def _run_haystack_update():
    """Update the Haystack index after prepping section paragraphs."""
    call_command('update_index', 'regulations3k', '--remove')


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Extract paragraphs and run Haystack's `update_index` command."""
        counter = {
            'created': 0,
            'deleted': 0,
            'kept': 0,
        }
        regulations = Part.objects.all()
        versions = [part.effective_version for part in regulations]
        sections = Section.objects.filter(subpart__version__in=versions)
        for section in sections:
            section_count = section.extract_graphs()
            for key in counter:
                counter[key] += section_count.get(key, 0)
        logger.info(
            "Section paragraphs have been extracted for {} regulations.\n"
            "{} were created, {} were unchanged, and {} were deleted.".format(
                regulations.count(),
                counter['created'],
                counter['kept'],
                counter['deleted']))
        _run_haystack_update()
