import json
from operator import itemgetter

from django.core.management.base import BaseCommand
from django.template import engines

from bs4 import BeautifulSoup

from mega_menu.models import Menu
from v1.models import MenuItem


try:
    from wagtail.core.models import Site
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.models import Site


def int_or_none(value):
    return int(value) if value is not None else None


def generate_featured_links_from_menu_item(menu_item):
    blocks = filter(
        lambda block: block['type'] == 'featured_content',
        menu_item.column_4.stream_data
    )

    values = map(itemgetter('value'), blocks)

    for value in values:
        link = value['link']

        soup = BeautifulSoup(value['body'], 'html.parser')
        body = soup.text.strip()

        image = value.get('image', {}).get('upload')

        yield {
            'page': int_or_none(link['page_link']),
            'text': link['link_text'] or None,
            'url': link['external_link'] or None,
            'body': body,
            'image': image,
        }


def generate_other_links_from_menu_item(menu_item):
    for value in map(itemgetter('value'), menu_item.nav_footer.stream_data):
        soup = BeautifulSoup(value['content'], 'html.parser')
        for p in soup.findAll('p'):
            link = p.contents[-1]

            if len(p.contents) > 1:
                page = link['id'] if link['linktype'] == 'page' else None

                yield {
                    'page': int_or_none(page),
                    'text': p.contents[0].strip(),
                    'url': link['href'] if not page else None,
                    'icon': 'web',
                }
            else:
                yield {
                    'page': None,
                    'text': link.text,
                    'url': link['href'],
                    'icon': 'web',
                }


def generate_submenu_column_blocks_from_menu_item(menu_item):
    for i in range(1, 5):
        column = getattr(menu_item, 'column_%d' % i).stream_data

        blocks = filter(lambda block: block['type'] == 'nav_group', column)

        try:
            content = next(blocks)['value']
        except StopIteration:
            continue

        yield {
            'heading': (
                (not content['hide_group_title']) and content['group_title']
                or None
            ),
            'links': [
                {
                    'page': int_or_none(link['page_link']),
                    'text': link['link_text'] or None,
                    'url': link['external_link'] or None,
                } for link in map(itemgetter('link'), content['nav_items'])
            ],
        }


def menu_item_to_submenu_block(menu_item):
    return {
        'title': menu_item.link_text,
        'overview_page': menu_item.page_link_id,
        'featured_links': list(
            generate_featured_links_from_menu_item(menu_item)
        ),
        'other_links': list(generate_other_links_from_menu_item(menu_item)),
        'columns': list(
            generate_submenu_column_blocks_from_menu_item(menu_item)
        ),
    }


def migrate_english_menu():
    submenus = [
        {
            'type': 'submenu',
            'value': menu_item_to_submenu_block(menu_item),
        } for menu_item in MenuItem.objects.all()
    ]

    Menu.objects.update_or_create(
        language='en',
        defaults={'submenus': json.dumps(submenus)}
    )


def migrate_spanish_menu():
    jinja = engines['wagtail-env']
    template = jinja.get_template(
        '_includes/organisms/_vars-mega-menu-spanish.html'
    )
    menu_items = template.template.module.menu_items

    root_page = Site.objects.get(is_default_site=True).root_page

    submenus = [
        {
            'type': 'submenu',
            'value': {
                'title': menu_item['link_text'],
                'overview_page': root_page.route(None, [
                    c for c in menu_item['external_link'].split('/') if c
                ])[0].pk,
            },
        } for menu_item in menu_items
    ]

    Menu.objects.update_or_create(
        language='es',
        defaults={'submenus': json.dumps(submenus)}
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        migrate_english_menu()
        migrate_spanish_menu()
