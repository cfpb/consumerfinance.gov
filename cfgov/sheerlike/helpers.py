from elasticsearch import Elasticsearch


class IndexHelper(object):
    # See "The borg singleton" in "Learning Python Design Patterns"
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(IndexHelper, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

    def configure(self, config):
        self.es = Elasticsearch(config["elasticsearch"])
        self.index_name = config['index']
