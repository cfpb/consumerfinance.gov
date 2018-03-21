from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from haystack.fields import CharField as BaseCharField


class CharFieldWithSynonyms(BaseCharField):

    def __init__(self, language='en', **kwargs):
        synonym_analyzer = 'synonym_{language}'.format(language=language)
        # Ensure that the synonym analyzer is available
        index_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS')
        if (synonym_analyzer not in
                index_settings['settings']['analysis']['analyzer']):
            raise ImproperlyConfigured(
                "CharFieldWithSynonyms requires a synonym analyzer for "
                "{language} (named {name}) to be configured".format(
                    language=language, name=synonym_analyzer))

        self.analyzer = synonym_analyzer
        super(CharFieldWithSynonyms, self).__init__(**kwargs)
