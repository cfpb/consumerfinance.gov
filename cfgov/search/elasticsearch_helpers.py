import os

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
synonym_home = '/src/cfgov/current/cfgov/search/resources' if os.environ.get('USE_AWS_ES', False) else '/usr/share/elasticsearch/config/synonyms'
synonym_file_en = open(f'{synonym_home}/synonyms_en.txt')
synonyms_en = [line.rstrip('\n') for line in synonym_file_en]
synonym_file_en.close()

synonym_es_file = open(f'{synonym_home}/synonyms_es.txt')
synonyms_es = [line.rstrip('\n') for line in synonym_file_es]
synonym_es_file.close()

synonyms = synonyms_en.append(synonyms_es)

synonynm_filter = token_filter(
    'synonym_filter',
    'synonym',
    synonyms=synonyms
)

synonym_analyzer = analyzer(
    'synonym_analyzer_en',
    type='custom',
    tokenizer='standard',
    filter=[
        synonynm_filter,
        'lowercase'
    ])
