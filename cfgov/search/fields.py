from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from haystack.fields import CharField as BaseCharField


class CharFieldWithSynonyms(BaseCharField):

    def __init__(self, **kwargs):
        # Ensure that the synonym analyzer is available
        index_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS')
        if 'synonym' not in index_settings['settings']['analysis']['analyzer']:
            raise ImproperlyConfigured(
                "CharFieldWithSynonyms requires a synonym analyzer to be "
                "configured")

        self.analyzer = 'synonym'
        super(CharFieldWithSynonyms, self).__init__(**kwargs)
