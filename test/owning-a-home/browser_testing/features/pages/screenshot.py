from datetime import datetime


class Screenshot(object):
    """This class formats the file name of the screenshot

    The current timestamp is added to the file prefix to create the filename
    The filename is passed to the get_screenshot method of the base class
    """

    def __init__(self, base, take_screenshots=True,
                 filename_prefix=u'Screenshot'):
        self.take_screenshots = take_screenshots
        self.base = base
        self.filename_prefix = filename_prefix

    def save(self, filename=''):
        if not self.take_screenshots:
            return

        if filename == '':
            filename = '%s_%s' % (self.filename_prefix, self.build_timestamp())

        self.base.get_screenshot(filename)

    def build_timestamp(self):
        return datetime.now().isoformat()
