from v1.models.learn_page import EnforcementActionPage, EnforcementActionStatus
from v1.util.ref import enforcement_statuses


def get_value(label):
    for status in enforcement_statuses:
        if label == status[1]:
            return status[0]


def resave_enforcement():
    draft_pages = []
    for page in EnforcementActionPage.objects.all():
        url = page.get_url()

        if not page.live:
            continue
        if 'policy-compliance/enforcement/actions' not in url:
            continue
        if page.has_unpublished_changes:
            draft_pages.append(url)
            continue

        page.statuses.set([EnforcementActionStatus(
            institution=stat.institution,
            status=get_value(stat.status)
        ) for stat in page.statuses.all()])

        page.save()

    if len(draft_pages) > 0:
        print('Skipped the following draft pages:', ' '.join(draft_pages))
    else:
        print('No draft pages found, all valid enforcement pages updated')


def run():
    resave_enforcement()
