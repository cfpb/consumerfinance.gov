import re
from itertools import chain


REGEX_REMOVE_QUERY_STRING = re.compile(r"\?.*$")


class FrontendConverter:
    def __init__(self, menu, request=None):
        self.menu = menu
        self.request = request

    def get_menu_items(self):
        self._submenu_selected = False
        self._link_selected = False

        return [
            self._get_menu_item(submenu.value)
            for submenu in self.menu.submenus
        ]

    def _get_menu_item(self, submenu):
        # Normally we want to mark menu links as selected if the current
        # request is either on that link or one of its children; this lets us
        # properly highlight the menu if on the child of a menu link. But we
        # don't want to do this for overview links, which may be the parent
        # of all links beneath them.
        overview_link = self.make_link(
            {
                "page": submenu.get("overview_page"),
                "text": submenu.get("title"),
            },
            selected_exact_only=True,
        )

        menu_item = {"overview": overview_link}

        columns = self.get_columns(submenu)
        if columns:
            menu_item["nav_groups"] = columns

        featured_links = self.make_links(submenu.get("featured_links"))
        if featured_links:
            menu_item["featured_items"] = featured_links

        other_links = self.make_links(submenu.get("other_links"))
        if other_links:
            menu_item["other_items"] = other_links

        if not self._submenu_selected:
            # If the current request either matches or is a child of this
            # menu's links (overview, other, and columns, deliberately
            # excluding featured), then we mark this menu as selected.
            for link in chain(
                [overview_link],
                other_links,
                *chain(column["nav_items"] for column in columns),
            ):
                url = link.get("url")
                if url:
                    url_no_query_string = REGEX_REMOVE_QUERY_STRING.sub(
                        "", url
                    )

                    if self.request.path.startswith(url_no_query_string):
                        menu_item["selected"] = True
                        self._submenu_selected = True
                        break

        return menu_item

    def get_columns(self, submenu):
        columns = []
        last_heading = None

        for column in submenu.get("columns") or []:
            heading = column.get("heading")

            columns.append(
                {
                    "title": heading or last_heading,
                    "title_hidden": not heading,
                    "nav_items": [
                        self.make_link(link)
                        for link in (column.get("links") or [])
                    ],
                }
            )

            last_heading = heading

        return columns

    def make_links(self, values):
        return list(map(self.make_link, values)) if values else []

    def make_link(self, value, selected_exact_only=False):
        page = value.get("page")
        text = value.get("text")
        icon = value.get("icon")

        if page:
            url = page.get_url(request=self.request)

            link = {
                "url": url,
                "text": text or page.title,
            }
        else:
            link = {"text": text}

            url = value.get("url")
            if url:
                link["url"] = url

        if icon:
            link["icon"] = icon

        if not self._link_selected:
            if selected_exact_only:
                selected = url and self.request.path == url
            else:
                selected = url and self.request.path.startswith(url)

            if selected:
                link["selected"] = True
                self._link_selected = True

        return link
