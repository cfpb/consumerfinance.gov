from urllib import urlencode

from django.core.signing import Signer
from django.core.urlresolvers import reverse


def append_query_args_to_url(base_url, args_dict):
    return "{0}?{1}".format(base_url, urlencode(args_dict))


def sign_url(url, secret=None):
    if secret:
        signer = Signer(secret, sep='||')
    else:
        signer = Signer(sep='||')

    url, signature = signer.sign(url).split('||')
    return (url, signature)


def signed_redirect(url):
    url, signature = sign_url(url)
    query_args = {'ext_url': url,
                  'signature': signature}

    return ('{0}?{1}'.format(reverse('external-site'), urlencode(query_args)))


def unsigned_redirect(url):
    query_args = {'ext_url': url}
    return ('{0}?{1}'.format(reverse('external-site'), urlencode(query_args)))


def extract_answers_from_request(request):
    answers = [(param.split('_')[1], value) for param, value in
               request.POST.items() if param.startswith('questionid')]
    return answers


def slice_list(l, n):
    start = 0
    for i in xrange(n):
        stop = start + len(l[i::n])
        chunk = l[start:stop]

        if chunk:
            yield chunk

        start = stop
