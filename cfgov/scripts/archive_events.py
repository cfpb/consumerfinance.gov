from v1.models.learn_page import EventPage
from v1.models.browse_filterable_page import BrowseFilterablePage, EventArchivePage

from django.utils import timezone
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


def run():
    logger.info('Searching for events to archive...')
    event_page_exists = BrowseFilterablePage.objects.filter(title='Events').exists()
    archive_event_page_exists = EventArchivePage.objects.filter(title__icontains='Archive').exists()

    if event_page_exists and archive_event_page_exists:
        events = BrowseFilterablePage.objects.get(title='Events')
        archived_events = EventArchivePage.objects.get(title__icontains='Archive')

        if len(events.get_children()) > 1:
            for child in events.get_children():
                event = child.specific
                if isinstance(event, EventPage):
                    if event.end_dt:
                        if event.end_dt < timezone.now():
                            if event.can_move_to(archived_events):
                                event.move(archived_events, pos='last-child')
                                logger.info(event.title + ' Event .....archived')
        else:
            logger.info('No events to archive found....')
    elif not event_page_exists:
        logger.info('Events browse filterable page has not been created....')
    elif not archive_event_page_exists:
        logger.info('No Archived events Browse filterable page named \'Archive\' exist....')
    else:
        logger.info('No events exist in the database...')
