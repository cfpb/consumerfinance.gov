import time


class Utils(object):

    def __init__(self, default_delay_secs=0):
        self.default_delay_secs = default_delay_secs
        self.time_spent_sleeping = 0

    def zzz(self, secs=0):
        if secs > 0:
            print("ZZZZZZZZZing for %s secs" % secs)
            time.sleep(secs)
            self.time_spent_sleeping += secs
        elif self.default_delay_secs > 0:
            print("ZZZZZZZZZing for %s secs" % self.default_delay_secs)
            time.sleep(self.default_delay_secs)
            self.time_spent_sleeping += self.default_delay_secs

    def build_url(self, base_url, relative_url=''):
        if relative_url == '':
            return base_url.strip()
        elif relative_url.startswith('/'):
            return '%s%s'.strip() % (base_url, relative_url)
        else:
            return '%s/%s'.strip() % (base_url, relative_url)

    def strip_trailing_slash(self, url):
        if url.endswith("/"):
            return url[:-1]
        return url

    def urls_match(self, url1, url2):
        return (self.strip_trailing_slash(url1) ==
                self.strip_trailing_slash(url2))
