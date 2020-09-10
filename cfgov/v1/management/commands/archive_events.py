import logging

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.utils import timezone

from v1.models.browse_filterable_page import (
    BrowseFilterablePage, EventArchivePage
)
from v1.models.learn_page import EventPage


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Move event pages whose end date has passed into the archive'

    def handle(self, *args, **options):
        logger.info('Searching for events to archive…')
        event_page_exists = BrowseFilterablePage.objects.filter(
            title='Events'
        ).exists()
        archive_event_page_exists = EventArchivePage.objects.filter(
            title__icontains='Archive'
        ).exists()

        if event_page_exists and archive_event_page_exists:
            events = BrowseFilterablePage.objects.get(title='Events')
            archive = EventArchivePage.objects.get(
                title__icontains='Archive')

            live_event_pages = events.get_children().live().type(EventPage)

            if len(live_event_pages) > 1:
                for event in live_event_pages:
                    event = event.specific
                    if event.end_dt:
                        if event.end_dt < timezone.now():
                            if event.can_move_to(archive):
                                try:
                                    event.move(archive, pos='last-child')
                                except ValidationError:
                                    isodate = event.start_dt.date().isoformat()
                                    event.slug = event.slug + '-' + isodate
                                    event.save()
                                    event.move(archive, pos='last-child')
                                # No longer logging here because event.move has
                                # its own log statement.
            else:
                logger.info('No past events to be archived were found.')
        elif not event_page_exists:
            logger.info('BrowseFilterablePage titled "Events" does not exist.')
        elif not archive_event_page_exists:
            logger.info(
                'EventArchivePage with "Archive" in the title does not exist.'
            )
