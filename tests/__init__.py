import os
import json

from elasticsearch import Elasticsearch

index_name = "cfgov_test"
root = os.getcwd()

def setup_package():
    es = Elasticsearch()
    if es.indices.exists(index_name):
        es.indices.delete(index_name)
    es.indices.create(index=index_name)

    # Create the mappings
    create_mapping('newsroom', '_settings/posts_mappings.json')
    create_mapping('watchroom', '_settings/posts_mappings.json')

    # Index the documents
    index_documents('newsroom', 'tests/fixtures/newsroom.json')
    index_documents('views', 'tests/fixtures/views.json')
    index_documents('watchroom', 'tests/fixtures/watchroom.json')

def teardown_package():
    es = Elasticsearch()
    es.indices.delete(index_name)

def create_mapping(doc_type, mapping_json_path):
    es = Elasticsearch()
    mapping_json = open(os.path.join(root, mapping_json_path))
    mapping = json.load(mapping_json)
    es.indices.put_mapping(index=index_name,
                           doc_type=doc_type,
                           body={doc_type: mapping})

def index_documents(doc_type, json_path):
    es = Elasticsearch()
    json_file = open(os.path.join(root, json_path))
    documents = json.load(json_file)

    for document in documents:
        es.create(index=index_name,
                  doc_type=doc_type,
                  id=document['_id'],
                  body=document)