import os
import json

from django.contrib.syndication.views import Feed
from django.http import Http404

from sheerlike.query import QueryFinder

PARAM_TOKEN = '$$'


class SheerlikeFeed(Feed):
    doc_type = None

    def title(self):
        return self.settings.get('feed_title')

    def link(self):
        return self.settings.get('feed_url')

    def items(self, obj):
        return obj.search()

    def item_link(self, item):
        return self.get_field_value(item, 'entry_url')

    def item_title(self, item):
        return self.get_field_value(item, 'entry_title')

    def item_description(self, item):
        return self.get_field_value(item, 'entry_content')

    def item_author_name(self, item):
        author = self.get_field_value(item, 'entry_author')
        return author[0] if isinstance(author, list) else author

    def item_updateddate(self, item):
        return self.get_field_value(item, 'entry_updated')

    def get_object(self, request, *args, **kwargs):
        if kwargs.get('doc_type'):
            self.doc_type = kwargs.get('doc_type')
        query_finder = QueryFinder()
        query = getattr(query_finder, self.doc_type)
        if not query:
            raise Http404
        self.settings_file = query.filename
        self.settings = self.get_settings()
        return query

    def get_field_value(self, item, param):
        setting = self.settings.get(param)
        if setting:
            return getattr(item, setting.replace(PARAM_TOKEN, ''))

    def get_settings(self):
        if os.path.isfile(self.settings_file):
            with open(self.settings_file) as json_file:
                data = json.load(json_file)
                return data.get('feed')
        else:
            raise Exception('Unable to find feed settings file')
