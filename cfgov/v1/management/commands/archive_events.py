from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from v1.models.browse_filterable_page import (
    BrowseFilterablePage,
    EventArchivePage,
)
from v1.models.learn_page import EventPage


class Command(BaseCommand):
    help = "Move event pages whose end date has passed into the archive"

    def handle(self, *args, **options):
        self.stdout.write("Searching for events to archive…")
        event_page_exists = BrowseFilterablePage.objects.filter(title="Events").exists()
        archive_event_page_exists = EventArchivePage.objects.filter(
            title__icontains="Archive"
        ).exists()

        if not event_page_exists or not archive_event_page_exists:
            raise CommandError(
                "Error: Main events page and/or archive page not found. "
                "Please ensure that there is a BrowseFilterablePage named "
                '"Events" and an EventArchivePage with "Archive" in the name '
                "in order for this script to run correctly."
            )

        events = BrowseFilterablePage.objects.get(title="Events")
        archive = EventArchivePage.objects.get(title__icontains="Archive")
        live_event_pages = events.get_children().live().type(EventPage)
        events_archived = False

        if live_event_pages:
            for event in live_event_pages:
                event = event.specific

                if event.end_dt:
                    end_dt = event.end_dt
                else:
                    end_dt = event.start_dt

                if end_dt < timezone.now():
                    if event.can_move_to(archive):
                        try:
                            event.move(archive, pos="last-child")
                        except ValidationError:
                            iso_date = event.start_dt.date().isoformat()
                            event.slug = event.slug + "-" + iso_date
                            event.save()
                            event.move(archive, pos="last-child")
                        # Not logging here because event.move writes its
                        # own log to stdout.
                        events_archived = True

            if not events_archived:
                self.stdout.write("No past events found to be archived.")

        else:
            self.stdout.write("No live event pages found.")
