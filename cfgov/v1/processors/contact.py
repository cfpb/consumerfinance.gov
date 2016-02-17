import dateutil

from core.management.commands._helpers import SnippetDataConverter
from ..models.snippets import Contact
import hashlib


class DataConverter(SnippetDataConverter):
    def convert(self, doc):

        post_dict = {
            'heading': doc.get('title') + ';;' + doc.get('slug'),
            'body': doc.get('content', u''),
        }

        # Stream Fields
        stream_index = 0

        # ---- Phone -------
        phone_index = 0
        if doc.get('fax'):
            if doc.get('fax').get('num'):
                post_dict = phone_formatter(post_dict, stream_index, phone_index, True, doc.get('fax').get('num'))
                phone_index += 1

        if doc.get('phone'):
            for phone in doc.get('phone'):
                if stream_index > 0:
                    post_dict = phone_formatter(post_dict, (stream_index - 1), phone_index, False, phone.get('num'))
                else:
                    post_dict = phone_formatter(post_dict, stream_index, phone_index, False, phone.get('num'))
                phone_index += 1

        if phone_index > 0:
            stream_index += 1

        # ----- Email -----
        email_index = 0
        if doc.get('email'):
            for email in doc.get('email'):
                post_dict = email_formatter(post_dict, stream_index, email_index,
                                            email.get('addr', u''), email.get('desc', u'email'))

                email_index += 1

        if email_index > 0:
            stream_index += 1

        # ---- Address ----
        if doc.get('street'):
            post_dict = street_formatter(post_dict, stream_index,
                                         doc.get('addr_desc', u'address'), doc.get('street', u''), doc.get('city', u''),
                                         doc.get('state', u''), doc.get('zip_code', u''))
            stream_index += 1

        post_dict['contact_info-count'] = str(stream_index)

        return post_dict

    def get_existing_snippet(self, doc):
        try:
            return Contact.objects.get(hash=hashlib.md5(doc.get('title') + ';;' + doc.get('slug')).hexdigest())
        except Contact.DoesNotExist:
            return None


stream_group = 'contact_info-'


def phone_formatter(dict, index, pindex, is_fax, number):
    dict[stream_group + str(index) + '-deleted'] = u''
    dict[stream_group + str(index) + '-order'] = str(index)
    dict[stream_group + str(index) + '-type'] = u'phone'

    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-deleted'] = u''
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-order'] = str(pindex)
    if is_fax:
        dict[stream_group + str(index) + '-value-fax'] = 'on'
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-value-number'] = number
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-value-tty'] = u''
    dict[stream_group + str(index) + '-value-phones-' + str(pindex) + '-value-vanity'] = u''
    dict[stream_group + str(index) + '-value-phones-count'] = str((pindex + 1))

    return dict


def email_formatter(dict, index, eindex, email, label):
    dict[stream_group + str(index) + '-deleted'] = u''
    dict[stream_group + str(index) + '-order'] = str(index)
    dict[stream_group + str(index) + '-type'] = u'email'

    dict[stream_group + str(index) + '-value-emails-' + str(eindex) + '-deleted'] = u''
    dict[stream_group + str(index) + '-value-emails-' + str(eindex) + '-order'] = u'0'
    dict[stream_group + str(index) + '-value-emails-' + str(eindex) + '-value-url'] = email
    dict[stream_group + str(index) + '-value-emails-' + str(eindex) + '-value-text'] = label
    dict[stream_group + str(index) + '-value-emails-count'] = str((eindex + 1))

    return dict


def street_formatter(dict, index, label, street, city, state, zip_code):
    dict[stream_group + str(index) + '-deleted'] = u''
    dict[stream_group + str(index) + '-order'] = str(index)
    dict[stream_group + str(index) + '-type'] = u'address'

    if not label:  # Empty string check
        label = 'address'

    dict[stream_group + str(index) + '-value-label'] = label
    dict[stream_group + str(index) + '-value-street'] = street
    dict[stream_group + str(index) + '-value-city'] = city
    dict[stream_group + str(index) + '-value-state'] = state
    dict[stream_group + str(index) + '-value-zip_code'] = zip_code

    return dict
