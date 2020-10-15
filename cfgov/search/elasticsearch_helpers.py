from django.conf import settings
import re

from elasticsearch_dsl import analyzer, token_filter, tokenizer

from search.models import Synonym


def strip_html(markup):
    """
    Make sure markup stripping doesn't mash content elements together.

    Also remove no-break space characters.
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, " ", markup).strip().replace("\xa0", "")


UNSAFE_CHARACTERS = [
    '#', '%', ';', '^', '~', '`', '|',
    '<', '>', '[', ']', '{', '}', '\\'
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, '')
    return term


label_autocomplete = analyzer(
    'label_autocomplete',
    tokenizer=tokenizer(
        'trigram',
        'edge_ngram',
        min_gram=2,
        max_gram=25,
        token_chars=["letter", "digit"]
    ),
    filter=['lowercase', token_filter('ascii_fold', 'asciifolding')]
)


def get_synonyms():
    try:
        return list(Synonym.objects.values_list('synonym', flat=True))
    except Exception:
        return []


synonym_filter = token_filter(
    'synonym_filter',
    'synonym',
    synonyms=get_synonyms()
)

synonym_analyzer = analyzer(
    'synonym_analyzer',
    type='custom',
    tokenizer='standard',
    filter=[
        synonym_filter,
        'lowercase'
    ])


def environment_specific_index(base_name):
    if settings.DEPLOY_ENVIRONMENT in (None, '', 'local', 'production'):
        return base_name
    else:
        return f'{settings.DEPLOY_ENVIRONMENT}-{base_name}'
