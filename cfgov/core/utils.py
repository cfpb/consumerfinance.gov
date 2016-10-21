import hashlib
import base64

def hash_for_script(js):
    hasher = hashlib.sha256()
    hasher.update(js)
    encoded = base64.b64encode(hasher.digest())
    return "'sha256-{encoded}'".format(encoded=encoded)


def extract_answers_from_request(request):
    answers = [(param.split('_')[1], value) for param, value in
               request.POST.items() if param.startswith('questionid')]
    return answers
