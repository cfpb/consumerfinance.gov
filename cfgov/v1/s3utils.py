from django.conf import settings


def https_s3_url_prefix():
    s3_url = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)

    if not s3_url:
        raise RuntimeError('AWS_STORAGE_BUCKET_NAME is not defined')

    return 'https://' + s3_url + '/'
