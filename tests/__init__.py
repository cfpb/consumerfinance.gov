import os
import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

index_name = "cfgov_test"
root = os.getcwd()


def setup_package():
    logging.basicConfig()
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    tracer = logging.getLogger('elasticsearch.trace')
    tracer.setLevel(logging.DEBUG)
    tracer.addHandler(logging.FileHandler('elasticsearch-py.txt'))
    es = Elasticsearch()
    if es.indices.exists(index_name):
        es.indices.delete(index_name)
    es.indices.create(index=index_name)

    newsroom_mapping = { "properties" :
          {
            "title" : {"type" : "string", "store" : "yes"},
            "text" : {"type" : "string", "store" : "yes"},
            "date" : {"type" : "date", "store": "yes"},
            "category" : {"type":"string", "index": "not_analyzed"},
            "author" : {"type":"string", "index":"not_analyzed"},
            "tags" : {"type":"string", "store": "yes", "index":"not_analyzed"},
            "excerpt" : {"type":"string", "store": "yes"},
            "custom_fields": {
                    "properties": {
                        "display_in_newsroom": {"type":"string", "index":"not_analyzed"}
                    }
            }
          }
        }

    # Create the mappings
    es.indices.put_mapping(index=index_name,
                           doc_type="newsroom",
                           body={"newsroom": newsroom_mapping})

    newsroom_json = open(os.path.join(root, 'fixtures/newsroom.json'))
    newsroom = json.load(newsroom_json)

    view_json = open(os.path.join(root, 'fixtures/views.json'))
    view = json.load(view_json)

    # Index the documents
    for document in newsroom:
        es.create(index=index_name,
                  doc_type="newsroom",
                  id=document['_id'],
                  body=document)

    for document in view:
        es.create(index=index_name,
                  doc_type="views",
                  id=document['_id'],
                  body=document)

    print "outer mapping here", IndicesClient(es).get_mapping(index='cfgov_test')


def teardown_package():
    pass
    # es = Elasticsearch()
    # es.indices.delete(index_name)