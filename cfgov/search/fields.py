from haystack.fields import CharField as BaseCharField


class CharFieldWithSynonyms(BaseCharField):
    def __init__(self, **kwargs):
        self.analyzer = 'synonym'
        super(CharFieldWithSynonyms, self).__init__(**kwargs)
