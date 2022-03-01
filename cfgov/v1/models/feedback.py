from django.db import models
from django.db.models import Q
from django.utils.encoding import force_str
from django.utils.timezone import localdate
from django.utils.translation import gettext_noop  # noqa

from wagtail.core.models import Page

from backports import csv


# These lines will ensure that these strings, which are entered in Wagtail,
# get picked up for translation by makemessages, and thus do not fail the
# check for missing/extra translations (tox -e validate-translations).
translate_this = gettext_noop("Was this page helpful to you?")  # noqa
translate_this_too = gettext_noop("Was this answer helpful to you?")  # noqa


class FeedbackQuerySet(models.QuerySet):
    def for_pages(self, pages, exclude=False):
        q = self._filter_by_pages_q(pages)

        if exclude:
            q = ~q

        return self.select_related("page").filter(q)

    def _filter_by_pages_q(self, pages):
        q = Q()

        for page in pages:
            q |= self._filter_by_page_q(page)

        return q

    def _filter_by_page_q(self, page):
        return Q(page__path__startswith=page.path) & Q(
            page__depth__gte=page.depth
        )

    def write_csv(self, f):
        headings = [
            "comment",
            "is_helpful",
            "page",
            "referrer",
            "submitted_on",
            "language",
        ]

        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow([field for field in headings])

        for feedback in self:
            # For legacy compatibility purposes, generated CSVs should contain
            # only the date feedback was submitted, and not the complete
            # timestamp. Timestamps are stored in the database as UTC, but
            # we want them to be exported in the Django default timezone
            # specified in settings.TIME_ZONE, which is America/New_York.
            feedback.submitted_on = localdate(feedback.submitted_on).strftime(
                "%Y-%m-%d"
            )

            writer.writerow(
                [
                    force_str(getattr(feedback, heading), strings_only=True)
                    for heading in headings
                ]
            )


class Feedback(models.Model):
    submitted_on = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        Page,
        related_name="feedback",
        null=True,
        on_delete=models.SET_NULL,
    )
    comment = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=8, blank=True, null=True)
    referrer = models.CharField(max_length=255, blank=True, null=True)
    is_helpful = models.BooleanField(blank=True, null=True)
    expect_to_buy = models.CharField(max_length=255, blank=True, null=True)
    currently_own = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)

    objects = FeedbackQuerySet.as_manager()

    class Meta:
        permissions = (
            ("export_feedback", "Can export feedback from the Wagtail admin"),
        )
