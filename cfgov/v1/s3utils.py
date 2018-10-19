from django.conf import settings


def get_s3_url_prefix(https):
    s3_url = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)

    if not s3_url:
        raise RuntimeError('AWS_STORAGE_BUCKET_NAME is not defined')

    if not https:
        return 'http://' + s3_url + '/'
    else:
        return 'https://s3.amazonaws.com/' + s3_url + '/'


def http_s3_url_prefix():
    return get_s3_url_prefix(https=False)


def https_s3_url_prefix():
    return get_s3_url_prefix(https=True)
