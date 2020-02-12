from __future__ import unicode_literals

from v1.models import DocumentDetailPage
from v1.util.migrations import get_stream_data, set_stream_data


def update_sidefoot():
    for page in DocumentDetailPage.objects.all():
        url = page.get_url()

        if not page.live:
            continue
        if 'policy-compliance/enforcement/actions' not in url:
            continue

        stream_data = get_stream_data(page, 'sidefoot')

        print('\n'.join(vars(page).keys()))
        break

def run():
    update_sidefoot()
