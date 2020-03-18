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
            'overview': self.make_link({
                'page': submenu.get('overview_page'),
                'text': submenu.get('title'),
            }),
        }

        columns = self.get_columns(submenu)
        if columns:
            menu_item['nav_groups'] = columns

        featured_links = self.make_links(submenu.get('featured_links'))
        if featured_links:
            menu_item['featured_items'] = featured_links

        other_links = self.make_links(submenu.get('other_links'))
        if other_links:
            menu_item['other_items'] = other_links

        return menu_item

    def get_columns(self, submenu):
        columns = []
        last_heading = None

        for column in (submenu.get('columns') or []):
            heading = column.get('heading')

            columns.append({
                'title': heading or last_heading,
                'title_hidden': not heading,
                'nav_items': [
                    self.make_link(link)
                    for link in (column.get('links') or [])
                ],
            })

            last_heading = heading

        return columns

    def make_links(self, values):
        if values:
            return list(map(self.make_link, values))

    def make_link(self, value):
        page = value.get('page')
        text = value.get('text')
        icon = value.get('icon')

        if page:
            return self.make_link_for_page(page, text=text, icon=icon)

        link = {'text': text}

        if icon:
            link['icon'] = icon

        url = value.get('url')
        if url:
            link['url'] = url

        return link

    def make_link_for_page(self, page, text=None, icon=None):
        link = {
            'url': page.get_url(request=self.request),
            'text': text or page.title,
        }

        if icon:
            link['icon'] = icon

        return link
