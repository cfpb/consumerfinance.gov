from __future__ import unicode_literals

import datetime
import logging
import sys

from django.utils import timezone

import pytz

from ask_cfpb.models import (
    AnswerAudiencePage, AnswerCategoryPage, AnswerLandingPage, AnswerPage,
    AnswerResultsPage, TagResultsPage
)


logger = logging.getLogger('wagtail.core')
logger.setLevel(logging.ERROR)
TZ = pytz.timezone('US/Eastern')
AWARE_NOW = timezone.now().astimezone(TZ)
YESTERDAY = AWARE_NOW - datetime.timedelta(days=1)


def publish_ask_pages():
    print("Setting page go_live_at dates to yesterady")
    count = 0
    for cls in [AnswerPage,
                AnswerAudiencePage,
                AnswerCategoryPage,
                AnswerLandingPage,
                AnswerResultsPage,
                TagResultsPage]:
        for page in cls.objects.all():
            count += 1
            page.go_live_at = YESTERDAY
            revision = page.save_revision(approved_go_live_at=YESTERDAY)
            revision.publish()
            sys.stdout.write('.')
            sys.stdout.flush()

    print('\nBackdated go_live_at dates '
          'and published {} pages\n'.format(count))


def run():
    publish_ask_pages()
