# Page Search

For page searches on consumerfinance.gov, we use Elasticsearch and the [django-opensearch-dsl](https://django-opensearch-dsl.readthedocs.io/en/latest/) library, which is a lightweight wrapper around [opensearch-dsl-py](https://opensearch.org/docs/latest/).

- [Indexing](#indexing)
  - [Elasticsearch index configuration](#elasticsearch-index-configuration)
  - [Django model information](#django-model-information)
  - [Custom fields](#custom-fields)
  - [Helpers](#helpers)
  - [Building the index](#building-the-index)
- [Searching](#searching)
  - [Autocomplete](#autocomplete)
  - [Suggestions](#suggestions)
- [References](#references)

## Indexing

For any of our Django apps that need to implement search for their Django models or [Wagtail page types](wagtail-pages.md), we include a `documents.py` file that defines the Elasticsearch documents that will [map the model or page to the Elasticsearch index](https://django-opensearch-dsl.readthedocs.io/en/latest/getting_started/#create-document-classes).

The `Document` class includes three things:

1. The [Elasticsearch index configuration](https://django-opensearch-dsl.readthedocs.io/en/latest/getting_started/#create-document-classes)
2. The Django model information
3. [Custom fields to index](https://django-opensearch-dsl.readthedocs.io/en/latest/fields/), and any preparation that they require

We'll use our [Ask CFPB answer search document as an example](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/ask_cfpb/documents.py) for each of these:

```python
from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry

@registry.register_document
class AnswerPageDocument(Document):
    pass
```

### Elasticsearch index configuration

The index configuration is provided by an `Index` subclass on the document class that defines the [django-opensearch-dsl index options](https://django-opensearch-dsl.readthedocs.io/en/latest/document/#index-subclass).

```python
from search.elasticsearch_helpers import environment_specific_index

class AnswerPageDocument(Document):

    class Index:
        name = environment_specific_index('ask-cfpb')
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
```

For index naming, we have a helper function, `environment_specific_index`, that will generate the index name specific to the deployment environment. This allows each index to be isolated to a deployment environment within an Elasticsearch cluster.

### Django model information

The Django model information is provided by a `Django` class on the document class that defines the model and any fields names to be indexed directly from the model. A `get_queryset` method can be overriden to perform any filtering on the model's queryset before content is indexed.

```python
from ask_cfpb.models.answer_page import AnswerPage

class AnswerPageDocument(Document):

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(live=True, redirect_to_page=None)

    class Django:
        model = AnswerPage

        fields = [
            'search_tags',
            'language',
        ]
```

The fields in `fields` will be indexed without any preparation/manipulation, directly as are stored on the model.

### Custom fields

Sometimes it might be desirable to index a field as an alternative type — say, the string that matches an integer for a Django field that species `choices`.

It might also be desirable to construct a field to index from multiple fields on the model, particularly for Wagtail pages with stream fields.

We may also want to specify Elasticsearch-specific [field properties](https://django-opensearch-dsl.readthedocs.io/en/latest/fields/#field-classes), like a custom analyzer.

To do so, we specify [custom fields](https://django-opensearch-dsl.readthedocs.io/en/latest/fields/#using-attr-argument) as attributes on the document class, with an `attr` argument that specifies the field on the model to reference.

```python
from django_opensearch_dsl import fields

from search.elasticsearch_helpers import synonym_analyzer

class AnswerPageDocument(Document):
    text = fields.TextField(attr="text", analyzer=synonym_analyzer)
```

The `attr` on the model can be a `@property` or a Django model field.

We can also do any data preparation/manipulation for fields using [`prepare_`-prefixed methods](https://django-opensearch-dsl.readthedocs.io/en/latest/fields/#using-prepare_field).

```python
from django_opensearch_dsl import fields

class AnswerPageDocument(Document):
    portal_topics = fields.KeywordField()

    def prepare_portal_topics(self, instance):
        return [topic.heading for topic in instance.portal_topic.all()]
```

### Helpers

We provide a few common helpers in `search.elasticsearch_helpers` for use in creating document classes:

- `environment_specific_index(base_name)`: Generate the index name for the `base_name` that is specific to the deployment environment. This allows each index to be isolated to a deployment environment within an Elasticsearch cluster.
- `ngram_tokenizer`: A reusable ngram analyzer for creating fields that [autocomplete terms](#autocomplete). This is used for type-ahead search boxes.
- `synonym_analyzer`: A reusable analyzer for creating fields that will match synonyms of a search term.

```python
from search.elasticsearch_helpers import (
    environment_specific_index,
    ngram_tokenizer,
    synonym_analyzer,
)
```

### Building the index

With the `Document` class created for your model in a `documents.py` module within a Django app listed in `INSTALLED_APPS`, all that is left to do is to use the [django-opensearch-dsl management commands](https://django-opensearch-dsl.readthedocs.io/en/latest/management/) to rebuild the index:

```shell
./cfgov/manage.py opensearch index --force rebuild [INDEX]
./cfgov/manage.py opensearch document --force --indices [INDEX] --refresh --parallel index
```

The above commands can also be run to rebuild the index for an app's models at any time.

Finally, the indexes for all apps can be rebuilt using:

```shell
./cfgov/manage.py opensearch index --force rebuild
./cfgov/manage.py opensearch document --force --refresh --parallel index
```

Conveniently, we have a shell script that invokes the above two commands to rebuild all indexes:

```shell
./index.sh
```

## Searching

The document class [provides a `search()` class method](https://django-opensearch-dsl.readthedocs.io/en/latest/getting_started/#search) that returns a [`Search` object](https://opensearch.org/docs/latest/opensearch/rest-api/search/). The `Search` object is opensearch-dsl-py's representation of Elasticsearch search requests.

To [query](https://django-opensearch-dsl.readthedocs.io/en/latest/getting_started/#search) for a specific term, for example:

```python
from ask_cfpb.documents import AnswerPageDocument

AnswerPageDocument.search().query(
    "match", text={"query": search_term, "operator": "AND"}
)
```

We can also [add a filter context](https://django-opensearch-dsl.readthedocs.io/en/latest/getting_started/#search) before querying, which we do to limit results to a specific language in Ask CFPB:

```python
from ask_cfpb.documents import AnswerPageDocument

search = AnswerPageDocument.search().filter("term", language=language)
search.query(
    "match", text={"query": search_term, "operator": "AND"}
)
```

### Autocomplete

For search box autocomplete, we use a field with our `ngram_tokenizer` analyzer and then issue a "match" search query for that field.

Using the Ask CFPB document search above, with its language filter context, this looks like:

```python
from search.elasticsearch_helpers import ngram_tokenizer

class AnswerPageDocument(Document):
    autocomplete = fields.TextField(analyzer=ngram_tokenizer)

search = AnswerPageDocument.search().filter("term", language=language)
search.query('match', autocomplete=search_term)
```

### Suggestions

For suggested spelling corrections for search terms, [the `Search` object has a `suggest()` method](https://opensearch.org/docs/latest/opensearch/rest-api/search/) that provides spelling suggestions for a given term on a given field.

Using the Ask CFPB document search above, with its language filter context, this looks like:

```python
from ask_cfpb.documents import AnswerPageDocument

search = AnswerPageDocument.search().filter("term", language=language)
search.suggest('suggestion', search_term, term={'field': 'text'})
```

## References

- [django-opensearch-dsl](https://django-opensearch-dsl.readthedocs.io/en/latest/)
- [opensearch-dsl](https://opensearch.org/docs/latest/)
