from elasticsearch_dsl import analyzer, token_filter, tokenizer

from search.models import Synonym


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


synonynm_filter = token_filter(
    'synonym_filter',
    'synonym',
    synonyms=get_synonyms()
)

synonym_analyzer = analyzer(
    'synonym_analyzer',
    type='custom',
    tokenizer='standard',
    filter=[
        synonynm_filter,
        'lowercase'
    ])
