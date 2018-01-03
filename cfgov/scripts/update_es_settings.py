from django.conf import settings

from elasticsearch import Elasticsearch


# This is run so the Elasticsearch index settings actually get updated with
# the new settings when they're changed. We're going to just put this as part
# of our deployment so it gets run before a sheer_index to prevent failed
# deployments.
def run():
    es = Elasticsearch(settings.SHEER_ELASTICSEARCH_SERVER)
    index_name = settings.SHEER_ELASTICSEARCH_INDEX

    if not es.indices.exists(index_name):
        print 'Index %s does not exist' % index_name
        return

    es_settings = settings.SHEER_ELASTICSEARCH_SETTINGS
    es.indices.close(index_name)
    es.indices.put_settings(es_settings, index_name)
    es.indices.open(index_name)
