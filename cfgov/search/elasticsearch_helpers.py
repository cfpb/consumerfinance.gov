from django.conf import settings
from elasticsearch_dsl import analyzer, token_filter, tokenizer


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

synonym_file_en = open(f'{settings.ELASTICSEARCH_SYNONYMS_HOME}/synonyms_en.txt')
synonyms_en = [line.rstrip('\n') for line in synonym_file_en]
synonym_file_en.close()

synonym_file_es = open(f'{settings.ELASTICSEARCH_SYNONYMS_HOME}/synonyms_es.txt')
synonyms_es = [line.rstrip('\n') for line in synonym_file_es]
synonym_file_es.close()

synonyms = synonyms_en + synonyms_es

synonynm_filter = token_filter(
    'synonym_filter',
    'synonym',
    synonyms=synonyms
)

synonym_analyzer = analyzer(
    'synonym_analyzer',
    type='custom',
    tokenizer='standard',
    filter=[
        synonynm_filter,
        'lowercase'
    ])
