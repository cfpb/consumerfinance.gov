from django.core.files.storage import FileSystemStorage


class SheerlikeStaticStorage(FileSystemStorage):

    def __init__(self, **kwargs):
        self.slug = kwargs['slug']
        del kwargs['slug']
        super(SheerlikeStaticStorage, self).__init__(**kwargs)

    def open(self, name, mode='rb'):
        corrected_name = name[len(self.slug) + 1:]
        return super(SheerlikeStaticStorage, self).open(corrected_name, mode)
