class FrontendConverter:
    def __init__(self, menu, request=None):
        self.menu = menu
        self.request = request

    def get_menu_items(self):
        return [
            self.get_menu_item(submenu.value) for submenu in self.menu.submenus
        ]

    def get_menu_item(self, submenu):
        menu_item = {
            'link': self.make_link({
                'page': submenu.get('overview_page'),
                'text': submenu.get('title'),
            }),
        }

        columns = self.get_columns(submenu)
        if columns:
            menu_item['nav_groups'] = columns

        # For legacy menu
        footer = self.get_footer(submenu)
        if footer:
            menu_item['footer'] = footer

        featured_content = self.get_featured_content(submenu)
        if featured_content:
            menu_item['featured_content'] = featured_content

        # For new menu variations
        featured_links = self.make_links(submenu.get('featured_links'))
        if featured_links:
            menu_item['featured_links'] = featured_links

        other_links = self.make_links(submenu.get('other_links'))
        if other_links:
            menu_item['other_links'] = other_links

        return menu_item

    def get_columns(self, submenu):
        columns = []
        last_heading = None

        for column in (submenu.get('columns') or []):
            heading = column.get('heading')

            columns.append({
                'value': {
                    'group_title': heading or last_heading,
                    'hide_group_title': not heading,
                    'nav_items': [
                        self.make_link(link)
                        for link in (column.get('links') or [])
                    ],
                },
            })

            last_heading = heading

        return columns

    def get_footer(self, submenu):
        footer_links = []

        for other_link in submenu.get('other_links') or []:
            page = other_link.get('page')

            if page:
                link = self.make_link_for_page(page)
                text = other_link['text']
                url = link['external_link']
                link_text = link['link_text']
            else:
                text = ''
                url = other_link['url']
                link_text = other_link['text']

            html = '<p>'

            if text:
                html += '<span aria-hidden="true">{}</span> '.format(text)

            html += '<a'

            if text:
                html += ' aria-label="{} {}"'.format(text, link_text)

            html += ' href="{}">{}</a></p>'.format(url, link_text)

            footer_links.append(html)

        return '\n'.join(footer_links)

    def get_featured_content(self, submenu):
        featured_links = submenu.get('featured_links')

        if featured_links:
            featured_link = featured_links[0]

            value = {'link': self.make_link(featured_link)}

            value.update({
                'body': featured_link['body'],
                'image': {
                    'url': (
                        featured_link['image'].get_rendition('original').url
                    ),
                },
            })

            return {'value': value}

    def make_links(self, values):
        if values:
            return list(map(self.make_link, values))

    def make_link(self, value):
        page = value.get('page')
        text = value.get('text')
        icon = value.get('icon')

        if page:
            return self.make_link_for_page(page, text=text, icon=icon)

        link = {'link_text': text}

        if icon:
            link['icon'] = icon

        url = value.get('url')
        if url:
            link['external_link'] = url

        return link

    def make_link_for_page(self, page, text=None, icon=None):
        link = {
            'external_link': page.get_url(request=self.request),
            'link_text': text or page.title,
        }

        if icon:
            link['icon'] = icon

        return link
