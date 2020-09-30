# Elasticsearch

We use Elasticsearch 7.4 and the [django-elasticsearch-dsl](https://django-elasticsearch-dsl.readthedocs.io/en/latest/) library to interact with Elasticsearch. 

## Implementing Elasticsearch for a Wagtail Page

In order to introduce consistency across the different apps within consumerfinance.gov we are encouraging the following structure for interacting with Elasticsearch. We are looking to organize all of our search related code to a sub directory within the respective apps models directory. A typical structure would look like `ask-cfpb/models/search/documents.py`, where ask-cfpb is the app where the search will reside in. Within the documents.py file we would expect to see the following classes.

### Wagtail Page

The first class to consider is the wagtail page, which is what our content editors will see and use from within the CMS. This is where we define all of our wagtail fields and should align with any other wagtail pages we leverage.

### Document Class

This class is a model of what we load into our elasticsearch index. It should define the various fields and their types as well as do any data preparation/manipulation prior to being saved in the Elasticsearch index. This class extends the django-elasticsearch-dsl `Document` class and should have a reference to the wagtail page within its django subclass. Below is an example document.

```python

@registry.register_document
class AnswerPageSearchDocument(Document):

    url = fields.TextField()

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(live=True, redirect_to_page=None)

    def prepare_search_tags(self, instance):
        return instance.clean_search_tags

    def prepare_url(self, instance):
        return instance.url

    class Index:
        name = 'ask-cfpb'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = AnswerPage

        fields = [
            'search_tags',
            'language',
        ]
```

### Search Class

The search class is responsible for interacting with Elasticsearch and performing queries. The goal is to define a single source for where we perform queries, and allow them to be invoked when needed from various views. Below is an example of a Search Class.

```python
class AnswerPageSearch:
    def __init__(self, search_term, language='en'):
        self.language = language
        self.search_term = make_safe(search_term).strip()

    def search(self):
        search = AnswerPageSearchDocument.search().filter(
                "term", language=self.language).query("match", text=self.search_term)
        total_results = search.count()
        search = search[0:total_results]
        response = search.execute()
        results = response[0:total_results]
        return {
            'search_term': self.search_term,
            'suggestion': None,
            'results': results
        }
```

