
from v1.models import CFGOVPageCategory, DocumentDetailPage
from v1.util.migrations import get_stream_data, set_stream_data


def get_new_name(current):
    stip = 'stipulation-and-consent-order-2'
    admin = 'administrative-adjudication-2'
    fed = 'fed-district-case'
    if current == stip or current == admin:
        return 'administrative-proceeding'
    elif current == fed:
        return 'civil-action'
    else:
        return current


def get_new_category(name):
    return CFGOVPageCategory(name=get_new_name(name))


def update_page_category(page):
    cats = page.categories.all()
    updated = [get_new_category(cat.name) for cat in cats]
    page.categories.set(updated)
    page.save()


def update_categories():
    draft_pages = []
    for page in DocumentDetailPage.objects.all():
        url = page.get_url()

        if not page.live:
            continue
        if 'policy-compliance/enforcement/actions' not in url:
            continue
        if page.has_unpublished_changes:
            draft_pages.append(url)
            continue

        stream_data = get_stream_data(page, 'sidefoot')

        # Remove inline Category, use the page category instead
        for field in stream_data:
            if field['type'] == 'related_metadata':
                field_content = field['value']['content']
                new_content = [
                    {'type': 'categories', 'value': {
                        'heading': 'Category',
                        'show_categories': True
                    }}
                ]
                for block in field_content:
                    if block['value'].get('heading', '') != 'Category':
                        new_content.append(block)
                    field['value']['content'] = new_content
            break

        set_stream_data(page.specific, 'sidefoot', stream_data)

        # Update page categories according to defined map
        update_page_category(page)

    if len(draft_pages) > 0:
        print('Skipped the following draft pages:', ' '.join(draft_pages))
    else:
        print('No draft pages found')
        print('Inline categories removed and page categories updated.')


def run():
    update_categories()
