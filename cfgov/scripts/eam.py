from __future__ import unicode_literals

from v1.models import DocumentDetailPage
from v1.models.learn_page import EnforcementActionPage
from v1.util.migrations import get_stream_data, set_stream_data

import json


def update_sidefoot():
    for page in DocumentDetailPage.objects.all():
        url = page.get_url()

        if not page.live:
            continue
        if 'policy-compliance/enforcement/actions' not in url:
            continue

        keys = vars(page)
        del keys['_state']
        del keys['_wagtail_cached_site_root_paths']

        page.delete()

        eap = EnforcementActionPage.objects.create(**keys)
        print(eap)


        #print('\n'.join(vars(page).keys()))
        break

def run():
    update_sidefoot()
