import dateutil

from core.management.commands._helpers import SnippetDataConverter
from ..models.snippets import Contact


class DataConverter(SnippetDataConverter):
    def convert(self, doc):

        post_dict = {
            'title': doc.get('title'),
            'slug': doc.get('slug'),
            'body': doc.get('content', u''),
        }
        tags = ''
        for tag in doc.get('tags'):
            if ' ' in tag:
                tag = '"%s"' % tag
            tags += tag + ', '
        if tags:
            tags = tags[0:-2]
        post_dict['tags'] = tags
        post_dict['authors'] = '"%s"' % doc.get('author', {}).get('name', '')

        # Stream Fields
        stream_index = 0
        phone_index = 0
        if doc.get('fax'):
            if doc.get('fax').get('num'):
                post_dict = phone_formatter(post_dict, stream_index, phone_index, 'contact_info-', 'on',
                                            doc.get('fax').get('num'))
                phone_index += 1

        if doc.get('phone'):
            for phone in doc.get('phone'):
                if stream_index > 0:
                    post_dict = phone_formatter(post_dict, (stream_index - 1), phone_index, 'contact_info-', 'off',
                                                phone.get('num'))
                else:
                    post_dict = phone_formatter(post_dict, stream_index, phone_index, 'contact_info-', 'off',
                                                phone.get('num'))
                phone_index += 1

        if phone_index > 0:
            stream_index += 1

        email_index = 0
        if doc.get('email'):
            for email in doc.get('email'):
                post_dict['contact_info-' + str(stream_index) + '-deleted'] = u''
                post_dict['contact_info-' + str(stream_index) + '-order'] = str(stream_index)
                post_dict['contact_info-' + str(stream_index) + '-type'] = u'email'

                post_dict['contact_info-' + str(stream_index) + '-value-emails-' + str(email_index) + '-deleted'] = u''
                post_dict['contact_info-' + str(stream_index) + '-value-emails-' + str(email_index) + '-order'] = u'0'
                post_dict['contact_info-' + str(stream_index) + '-value-emails-' + str(
                    email_index) + '-value-href'] = email.get('addr', u'')
                post_dict['contact_info-' + str(stream_index) + '-value-emails-' + str(
                    email_index) + '-value-label'] = email.get('desc', u'email')
                post_dict['contact_info-' + str(stream_index) + '-value-emails-count'] = str((email_index + 1))

                email_index += 1

        if email_index > 0:
            stream_index += 1

        if doc.get('street'):
            post_dict['contact_info-' + str(stream_index) + '-deleted'] = u''
            post_dict['contact_info-' + str(stream_index) + '-order'] = str(stream_index)
            post_dict['contact_info-' + str(stream_index) + '-type'] = u'address'

            post_dict['contact_info-' + str(stream_index) + '-value-label'] = doc.get('addr_desc', u'')
            post_dict['contact_info-' + str(stream_index) + '-value-street'] = doc.get('street', u'')
            post_dict['contact_info-' + str(stream_index) + '-value-city'] = doc.get('city', u'')
            post_dict['contact_info-' + str(stream_index) + '-value-state'] = doc.get('state', u'')
            post_dict['contact_info-' + str(stream_index) + '-value-street'] = doc.get('zip_code', u'')

            stream_index += 1

        post_dict['contact_info-count'] = str(stream_index)

        if doc.get('web_0'):
            post_dict['web'] = doc.get('web_0', u'')

        if doc.get('web'):
            if doc['web'].get('label') and doc['web'].get('url'):
                post_dict['web_label'] = doc['web'].get('label')
                post_dict['web_url'] = doc['web'].get('url')
            if doc.get('web').get('url'):
                post_dict['web_url'] = doc.get('web').get('url')
            if doc.get('web').get('label'):
                post_dict['web_label'] = doc.get('web').get('label')

        return post_dict

    def get_existing_snippet(self, doc):
        try:
            #import pdb; pdb.set_trace()
            return Contact.objects.get(slug=doc.get('slug'))
        except Contact.DoesNotExist:
            return None


def phone_formatter(dict, index, pindex, stream_group, is_fax, number):
    dict[stream_group + str(index) + '-deleted'] = u''
    dict[stream_group + str(index) + '-order'] = str(index)
    dict[stream_group + str(index) + '-type'] = u'phone'

    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-deleted'] = u''
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-order'] = str(pindex)
    dict[stream_group + str(index) + '-value-fax'] = is_fax
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-number'] = number
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-tty'] = u''
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-vanity'] = u''
    dict[stream_group + str(index) + '-value-phones-count'] = str((pindex + 1))

    return dict
