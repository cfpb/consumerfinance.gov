from django.conf import settings
from django.utils import six
from django.utils.functional import lazy


"""Custom S3 storage backends to store files in subfolders."""
def MediaRootS3BotoStorage():
    from storages.backends.s3boto import S3BotoStorage
    return S3BotoStorage(location=settings.AWS_S3_ROOT)


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
