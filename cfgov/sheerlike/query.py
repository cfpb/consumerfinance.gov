import datetime
import json
import os
from collections import namedtuple

from django.conf import settings
from django.utils.datastructures import MultiValueDict as MultiDict
from django.utils.http import urlencode

import elasticsearch
from dateutil import parser
from pytz import timezone
from unipath import Path

from .filters import filter_dsl_from_multidict
from .middleware import get_request
from .templates import _convert_date


ALLOWED_SEARCH_PARAMS = (
    'doc_type',
    'analyze_wildcard',
    'analyzer',
    'default_operator',
    'df',
    'explain',
    'fields',
    'indices_boost',
    'lenient',
    'allow_no_indices',
    'expand_wildcards',
    'ignore_unavailable',
    'lowercase_expanded_terms',
    'from_',
    'preference',
    'q',
    'routing',
    'scroll',
    'search_type',
    'size',
    'sort',
    'source',
    'stats',
    'suggest_field',
    'suggest_mode',
    'suggest_size',
    'suggest_text',
    'timeout',
    'version')


FakeQuery = namedtuple('FakeQuery', ['es', 'es_index'])


def mapping_for_type(typename, es, es_index):

    return es.indices.get_mapping(index=es_index, doc_type=typename)


def field_or_source_value(fieldname, hit_dict):
    if 'fields' in hit_dict and fieldname in hit_dict['fields']:
        return hit_dict['fields'][fieldname]

    if '_source' in hit_dict and fieldname in hit_dict['_source']:
        return hit_dict['_source'][fieldname]


def datatype_for_fieldname_in_mapping(
        fieldname,
        hit_type,
        mapping_dict,
        es,
        es_index):

    try:
        return mapping_dict[es_index]["mappings"][
            hit_type]["properties"][fieldname]["type"]
    except KeyError:
        return None


def coerced_value(value, datatype):
    if datatype is None or value is None:
        return value

    TYPE_MAP = {'string': unicode,
                'date': parser.parse,
                'dict': dict,
                'float': float,
                'long': float,
                'boolean': bool}

    coercer = TYPE_MAP[datatype]

    if isinstance(value, list):
        if value and isinstance(value[0], list):
            return [[coercer(y) for y in v] for v in value]
        else:
            return [coercer(v) for v in value] or ""
    else:
        return coercer(value)


class QueryHit(object):

    def __init__(self, hit_dict, es, es_index):
        self.hit_dict = hit_dict
        self.type = hit_dict['_type']
        self.es = es
        self.es_index = es_index
        self.mapping = mapping_for_type(self.type, es=es, es_index=es_index)

    def __str__(self):
        return str(self.hit_dict.get('_source'))

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, attrname):
        value = field_or_source_value(attrname, self.hit_dict)
        datatype = datatype_for_fieldname_in_mapping(
            attrname, self.type, self.mapping, self.es, self.es_index)
        return coerced_value(value, datatype)

    def json_compatible(self):
        hit_dict = self.hit_dict
        fields = hit_dict.get('fields') or hit_dict.get('_source', {}).keys()
        return dict((field, getattr(self, field)) for field in fields)


class QueryResults(object):

    def __init__(self, query, result_dict, pagenum=1):
        self.result_dict = result_dict
        self.total = int(result_dict['hits']['total'])
        self.query = query

        # confusing: using the word 'query' to mean different things
        # above, it's the Query object
        # below, it's Elasticsearch query DSL

        if 'query' in result_dict:
            self.size = int(result_dict['query'].get('size', '10'))
            self.from_ = int(result_dict['query'].get('from', 1))
            self.pages = self.total / self.size + \
                int(self.total % self.size > 0)
        else:
            self.size, self.from_, self.pages = 10, 1, 1

        self.current_page = pagenum

    def __iter__(self):
        if 'hits' in self.result_dict and 'hits' in self.result_dict['hits']:
            for hit in self.result_dict['hits']['hits']:
                query_hit = QueryHit(hit, self.query.es, self.query.es_index)
                yield query_hit

    def __getitem__(self, index):
        if 'hits' in self.result_dict and 'hits' in self.result_dict['hits']:
            for i, hit in enumerate(self.result_dict['hits']['hits']):
                if i == index:
                    return QueryHit(hit, self.query.es, self.query.es_index)

    def __len__(self):
        if 'hits' in self.result_dict and 'hits' in self.result_dict['hits']:
            return len(self.result_dict['hits']['hits'])

    def aggregations(self, fieldname):
        if "aggregations" in self.result_dict and \
                fieldname in self.result_dict['aggregations']:
            return self.result_dict['aggregations'][fieldname]['buckets']

    def json_compatible(self):
        response_data = {}
        response_data['total'] = self.result_dict['hits']['total']
        if self.size:
            response_data['size'] = self.size

        if self.from_:
            response_data['from'] = self.from_

        if self.pages:
            response_data['pages'] = self.pages
        response_data['results'] = [
            hit.json_compatible() for hit in self.__iter__()]
        return response_data

    def url_for_page(self, pagenum):
        request = get_request()
        current_args = request.GET
        args_dict = MultiDict(current_args)
        if pagenum != 1:
            args_dict['page'] = pagenum
        elif 'page' in args_dict:
            del args_dict['page']

        encoded = urlencode(args_dict, doseq=True)
        if encoded:
            url = "".join(
                [request.path, "?", urlencode(args_dict, doseq=True)])
            return url
        else:
            return request.path


class Query(object):

    def __init__(self, filename, es, es_index, json_safe=False):
        # TODO: make the no filename case work

        self.es_index = es_index
        self.es = es
        self.filename = filename
        self.__results = None
        self.json_safe = json_safe

    def get_tag_related_documents(self, tags, size=0, additional_args={}):
        query_file = json.loads(file(self.filename).read())
        doc_type = query_file['query']['doc_type']
        query_dict = {'sort': [{'date': {'order': 'desc'}}]}

        if not additional_args:
            query_dict['query'] = {'bool': {'should': []}}
            for tag in tags:
                query_dict['query']['bool']['should'].append(
                    {'match': {'tags.lower': tag.lower()}})

        else:
            filtered_query = json.loads(file(
                getattr(QueryFinder(), 'filtered_17').filename).read())
            query_dict['query'] = filtered_query

            query_dict_filtered = query_dict['query']['filtered']

            for tag in tags:
                query_dict_filtered['query']['bool']['should'].append(
                    {'term': {'tags.lower': tag.lower()}})

            for arg in additional_args:
                query_dict_filtered['filter']['or'].append(arg)

        if size:
            query_dict['size'] = size

        response = self.es.search(index=self.es_index, doc_type=doc_type,
                                  body=query_dict, analyzer='tag_analyzer')
        return QueryResults(self, response)

    def search(
            self,
            aggregations=None,
            use_url_arguments=True,
            size=10,
            pdf_print=False,
            **kwargs):
        query_file = json.loads(file(self.filename).read())
        query_dict = query_file['query']

        if pdf_print:
            query_dict['size'] = settings.ELASTICSEARCH_BIGINT
        '''
        These dict constructors split the kwargs from the template into filter
        arguments and arguments that can be placed directly into the query
        body. The dict constructor syntax supports python 2.6, 2.7, and 3.x
        If python 2.7, use dict comprehension and iteritems()
        With python 3, use dict comprehension and items() (items() replaces
        iteritems and is just as fast)
        '''
        filter_args = dict((key, value) for (key, value) in kwargs.items()
                           if key.startswith('filter_'))
        non_filter_args = dict((key, value) for (key, value) in kwargs.items()
                               if not key.startswith('filter_'))
        query_dict.update(non_filter_args)
        pagenum = 1

        # Add in filters from the template.
        new_multidict = MultiDict()
        # First add the url arguments if requested
        if use_url_arguments:
            request = get_request()
            new_multidict = MultiDict(request.GET.copy())
            args_flat = request.GET.copy()
        # Next add the arguments from the search() function used in the
        # template
        for key, value in filter_args.items():
            new_multidict.update({key: value})

        filters = filter_dsl_from_multidict(new_multidict)
        query_body = {}

        if aggregations:
            aggs_dsl = {}
            if isinstance(aggregations, str):
                aggregations = [aggregations]  # so we can treat it as a list
            for fieldname in aggregations:
                aggs_dsl[fieldname] = {'terms':
                                       {'field': fieldname, 'size': 10000}}
            query_body['aggs'] = aggs_dsl
        else:
            if use_url_arguments:
                if 'page' in args_flat:
                    try:
                        pagenum = int(args_flat['page'])
                    except ValueError:
                        pagenum = 1
                    args_flat['from_'] = int(query_dict.get(
                        'size', '10')) * (pagenum - 1)

                args_flat_filtered = dict(
                    [(k, v) for k, v in args_flat.items() if v])
                query_dict.update(args_flat_filtered)
            query_body['query'] = {'filtered': {'filter': {}}}
            if filters:
                query_body['query']['filtered']['filter'][
                    'and'] = [f for f in filters]

            if 'filters' in query_file:
                if 'and' not in query_body['query']['filtered']['filter']:
                    query_body['query']['filtered']['filter']['and'] = []
                for json_filter in query_file['filters']:
                    query_body['query']['filtered'][
                        'filter']['and'].append(json_filter)
        final_query_dict = dict(
            (k, v) for (
                k, v) in query_dict.items() if k in ALLOWED_SEARCH_PARAMS)
        final_query_dict['index'] = self.es_index
        final_query_dict['body'] = query_body
        response = self.es.search(**final_query_dict)
        response['query'] = query_dict
        return QueryResults(self, response, pagenum)

    def possible_values_for(self, field, **kwargs):
        results = self.search(aggregations=[field], **kwargs)
        return results.aggregations(field)


class QueryFinder(object):

    def __init__(self):
        self.es = elasticsearch.Elasticsearch(
            settings.SHEER_ELASTICSEARCH_SERVER)
        self.es_index = settings.SHEER_ELASTICSEARCH_INDEX
        self.searchpath = [Path(p).child('_queries')
                           for s, p in settings.SHEER_SITES.items()]

    def __getattr__(self, name):
        for dir in self.searchpath:
            query_filename = name + ".json"
            query_file_path = os.path.join(dir, query_filename)

            if os.path.exists(query_file_path):
                query = Query(query_file_path, self.es, self.es_index)
                return query


class QueryJsonEncoder(json.JSONEncoder):
    query_classes = [QueryResults, QueryHit]

    def default(self, obj):
        if type(obj) in (datetime.datetime, datetime.date):
            return obj.isoformat()
        if type(obj) in self.query_classes:
            return obj.json_compatible()

        return json.JSONEncoder.default(self, obj)


def more_like_this(hit, **kwargs):
    es = elasticsearch.Elasticsearch(settings.SHEER_ELASTICSEARCH_SERVER)
    es_index = settings.SHEER_ELASTICSEARCH_INDEX
    doctype, docid = hit.type, hit._id
    raw_results = es.mlt(
        index=es_index, doc_type=doctype, id=docid, **kwargs)

    # this is bad and I should feel bad
    # (I do)
    fake_query = FakeQuery(es, es_index)
    return QueryResults(fake_query, raw_results)


def get_document(doctype, docid):
    es = elasticsearch.Elasticsearch(settings.SHEER_ELASTICSEARCH_SERVER)
    es_index = settings.SHEER_ELASTICSEARCH_INDEX
    raw_results = es.get(index=es_index, doc_type=doctype, id=docid)
    return QueryHit(raw_results, es, es_index)


def when(starttime, endtime, streamtime=None):
    start = _convert_date(starttime, 'America/New_York')
    if streamtime:
        start = _convert_date(streamtime, 'America/New_York')
    end = _convert_date(endtime, 'America/New_York')
    if start > datetime.datetime.now(timezone('America/New_York')):
        return 'future'
    elif end < datetime.datetime.now(timezone('America/New_York')):
        return 'past'
    else:
        return 'present'
