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

synonym_file = open('cfgov/search/resources/synonyms_en.txt')
synonyms = [line.rstrip('\n') for line in synonym_file]

synonynm_filter = token_filter(
    'synonym_filter_en',
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
