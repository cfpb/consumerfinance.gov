import dateutil

from core.management.commands._helpers import PageDataConverter


class DataConverter(PageDataConverter):

    tag_counterparts = [
        ('Consumer response', 'Consumer Response'),
        ('Academic Research Council', 'Academic research council'),
        ('Online Resources', 'Online resources'),
        ('deceptive practices', 'Deceptive practices'),
        ('Civil Penalty Fund', 'Civil penalty fund'),
        ('Open for Suggestions', 'Open for suggestions'),
        ('careers', 'Careers'),
    ]

    def add_defaults(self, doc, post_dict):
        super(DataConverter, self).add_defaults(post_dict)
        post_dict['header-count'] = 0

        # Sidefoot
        post_dict.update({
            'content-0-type': u'content',
            'content-0-value': doc.get('content', '').decode('utf-8'),
            'content-0-order': u'0',
            'content-count': u'1',
            'content-0-deleted': u'',
            'sidefoot-count': u'2',
            'sidefoot-0-type': u'related_posts',
            'sidefoot-0-deleted': u'',
            'sidefoot-0-order': u'0',
            'sidefoot-0-value-relate_posts': u'on',
            'sidefoot-0-value-specific_categories-count': u'1',
            'sidefoot-0-value-specific_categories-0-value': u'',
            'sidefoot-0-value-limit': u'3',
            'sidefoot-0-value-show_heading': u'on',
            'sidefoot-0-value-specific_categories-0-order': u'0',
            'sidefoot-0-value-specific_categories-0-deleted': u'',
            'sidefoot-0-value-header_title': u'Further reading',
            'sidefoot-0-value-view_more-url': u'/',
            'sidefoot-0-value-view_more-text': u'',
            'sidefoot-1-type': u'email_signup',
            'sidefoot-1-deleted': u'',
            'sidefoot-1-order': u'1',
            'sidefoot-1-value-form_field-0-value-type': u'email',
            'sidefoot-1-value-form_field-0-deleted': u'',
            'sidefoot-1-value-gd_code': u'USCFPB_91',
            'sidefoot-1-value-form_field-0-order': u'0',
            'sidefoot-1-value-form_field-count': u'1',
            'sidefoot-1-value-form_field-0-value-info': u'<p>The information you provide will permit the Consumer Financial Protection Bureau to process your request or inquiry.\xa0<a href="http://privacy/privacy-policy/">See More</a></p>',  # noqa
            'sidefoot-1-value-form_field-0-value-btn_text': u'Sign Up',
            'sidefoot-1-value-heading': u'Stay Informed',
            'sidefoot-1-value-form_field-0-value-label': u'Email Address',
            'sidefoot-1-value-form_field-0-value-placeholder': u'example@mail.com',  # noqa
            'sidefoot-1-value-text': u'Subscribe to our email newsletter. We will update you on new blogs.',  # noqa
        })

    def set_date(self, date_str):
        dt = dateutil.parser.parse(date_str)
        return dt.strftime('%Y-%m-%d')

    def format_tags(self, doc_tags):
        tags = ''
        for i, tag in enumerate(doc_tags):
            for counterpart in self.tag_counterparts:
                if tag in counterpart[0]:
                    doc_tags[i] = counterpart[1]
        for tag in doc_tags:
            if ' ' in tag:
                tag = '"%s"' % tag
            tags += tag + ', '
        if tags:
            tags = tags[0:-2]
        return tags

    def convert(self, doc):
        post_dict = {
            'title': doc.get('title', ''),
            'slug': doc.get('slug', ''),
        }
        self.add_defaults(doc, post_dict)

        post_dict['preview_description'] = doc.get('excerpt',
                                                   '').decode('utf-8')
        post_dict['date_published'] = self.set_date(doc.get('date', ''))
        post_dict['tags'] = self.format_tags(doc.get('tags'))
        post_dict['authors'] = self.format_tags(doc.get('author'))

        return post_dict
