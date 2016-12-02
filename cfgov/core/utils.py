import hashlib
import base64

from django.core.signing import Signer
from django.http.request import QueryDict
from django.core.urlresolvers import reverse


signer = Signer(sep='||')


def hash_for_script(js):
    hasher = hashlib.sha256()
    hasher.update(js.encode('utf-8'))
    encoded = base64.b64encode(hasher.digest())
    return "'sha256-{encoded}'".format(encoded=encoded)


def add_js_hash_to_request(request, js):
        if not hasattr(request, 'script_hashes'):
            request.script_hashes = []
        hash = hash_for_script(js)
        request.script_hashes.append(hash)


def sign_url(url):
    url, signature = signer.sign(url).split('||')
    return (url, signature)


def signed_redirect(url):
    url, signature = sign_url(url)
    query_args = QueryDict(mutable=True)
    query_args['ext_url'] = url
    query_args['signature'] = signature

    return ('{0}?{1}'.format(reverse('external-site'), query_args.urlencode()))

def extract_answers_from_request(request):
    answers = [(param.split('_')[1], value) for param, value in
               request.POST.items() if param.startswith('questionid')]
    return answers
