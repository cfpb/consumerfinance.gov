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
            'dupes': [],
        }
        regulations = Part.objects.all()
        versions = [part.effective_version for part in regulations
                    if part.effective_version]
        sections = Section.objects.filter(subpart__version__in=versions)
        for section in sections:
            section_count = section.extract_graphs()
            for key in ['created', 'deleted', 'kept']:
                counter[key] += section_count.get(key, 0)
            counter['dupes'] += section_count['dupes']
        dupes = sorted(set(counter['dupes']))
        logger.info(
            "Section paragraphs have been extracted for {} regulations.\n"
            "{} were created, {} were unchanged, {} were deleted, and "
            "{} dupes were found".format(
                regulations.count(),
                counter['created'],
                counter['kept'],
                counter['deleted'],
                len(dupes)))
        if dupes:
            logger.info("These paragraph IDs were dupes: \n{}".format(
                "\n".join(dupes)))
        _run_haystack_update()
