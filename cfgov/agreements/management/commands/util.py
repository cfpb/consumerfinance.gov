import os

from agreements.models import Agreement, Issuer
from slugify import slugify


def clear_tables():
    Agreement.objects.all().delete()


def get_file_size(path):
    return os.path.getsize(path)


def update_issuer(name):
    try:
        issuer = Issuer.objects.get(name=name)
    except Issuer.DoesNotExist:
        issuer = Issuer()
    except Issuer.MultipleObjectsReturned:
        raise Exception('Multiple Issuers exist for %s' % name)

    issuer.name = name
    issuer.slug = slugify(name, to_lower=True)
    issuer.save()

    return issuer


def update_agreement(
        issuer=None,
        file_name=None,
        file_path=None,
        s3_location=None):
    try:
        agreement = Agreement.objects.get(file_name=file_name)
    except Agreement.DoesNotExist:
        agreement = Agreement()
    except Agreement.MultipleObjectsReturned:
        raise Exception('Multiple Agreements exist for %s' % file_name)

    agreement.issuer = issuer
    agreement.file_name = file_name
    agreement.uri = s3_location
    agreement.size = get_file_size(file_path) or 0
    agreement.description = file_name
    agreement.save()
    return agreement


def upload_to_s3(file_path, s3_dest_path):
    import tinys3
    AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

    conn = tinys3.Connection(
        AWS_S3_ACCESS_KEY_ID,
        AWS_S3_SECRET_ACCESS_KEY,
        tls=True,
        endpoint='s3.amazonaws.com')

    file = open(file_path, 'rb')
    conn.upload(s3_dest_path, file, AWS_STORAGE_BUCKET_NAME)
