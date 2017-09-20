__author__ = 'CFPBLabs'

import time


class Utils(object):

    def __init__(self, default_delay_secs=0):
        self.default_delay_secs = default_delay_secs

    def zzz(self, secs=0):
        if secs > 0:
            time.sleep(secs)
        elif (self.default_delay_secs > 0):
            time.sleep(self.default_delay_secs)

    def build_url(self, base_url, relative_url=''):
        if relative_url == '':
            return base_url
        else:
            return '%s/%s' % (base_url, relative_url)

    def convert_nickname_to_id(self, nickname):
        id = ''

        if nickname == 'search':
            id = 'q'
        elif nickname == 'card issuer':
            id = 'issuer_select_chzn'

        return id
