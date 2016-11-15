from __future__ import print_function

import json
import re


def post_process(documents):
    post_processors = (
        convert_http_images,
    )

    for document in documents:
        for post_process in post_processors:
            post_process(document)

        yield document


def convert_http_images(document):
    source = document['_source']

    img_re = '<img [^>]*src="http://"'

    for k, v in source.iteritems():
        vj = json.dumps(v)
        if re.match
        if 'img' in vj:
            print(document['_type'], k)
            print(v)
            import pdb; pdb.set_trace()

    # 'content', 'custom_fields', 'resource_sections'
