import dateutil
import datetime

from core.management.commands._helpers import PageDataConverter

from ..util.ref import categories


class DataConverter(PageDataConverter):

    def add_defaults(self, doc, post_dict):
        super(DataConverter, self).add_defaults(post_dict)
        post_dict['header-count'] = 0

        # Categories
        for i in range(len(doc['blog_category'])):
            post_dict['categories-'+str(i)+'-id'] = u''
            post_dict['categories-'+str(i)+'-DELETE'] = u''
            post_dict['categories-'+str(i)+'-ORDER'] = str(i+1)
            for categories_tuple in categories:
                if categories_tuple[0] == 'Blog':
                    for category_tuple in categories_tuple[1]:
                        if category_tuple[1] == doc[blog_category][i]:
                            post_dict['categories-'+str(i)+'-name'] = category_tuple[0]

        # Sidefoot
        post_dict.update({
            'sidefoot-count': '1',
            'sidefoot-0-type': 'related_posts',
            'sidefoot-0-deleted': '',
            'sidefoot-0-order': '0',
            'sidefoot-0-value-relate_posts': 'on',
            'sidefoot-0-value-specific_categories-count': '1',
            'sidefoot-0-value-specific_categories-0-value': '',
            'sidefoot-0-value-limit': '3',
            'sidefoot-0-value-show_heading': 'on',
            'sidefoot-0-value-specific_categories-0-order': '0',
            'sidefoot-0-value-specific_categories-0-deleted': '',
            'sidefoot-0-value-header_title': 'Further reading',
            'sidefoot-0-value-view_more-url': '/',
            'sidefoot-0-value-view_more-text': '',
        })

    def set_date(self, date_str):
        dt = dateutil.parser.parse(date_str)
        return dt.strftime('%Y-%m-%d')

    def format_tags(self, doc_tags):
        tags = ''
        for tag in doc_tags:
            if ' ' in tag:
                tag = '"%s"' % tag
            tags += tag + ', '
        if tags:
            tags = tags[0:-2]
        return tags

    def convert(self, doc):
        post_dict = {
            'title':   doc.get('title', ''),
            'slug':    doc.get('slug', ''),
            'content': doc.get('content', '').decode('utf-8'),
        }
        self.add_defaults(doc, post_dict)

        post_dict['post_preview_description'] = doc.get('excerpt', '')
        post_dict['date_published'] = self.set_date(doc.get('date', ''))
        post_dict['tags'] = self.format_tags(doc.get('tags'))
        post_dict['authors'] = self.format_tags(doc.get('author'))

        return post_dict
