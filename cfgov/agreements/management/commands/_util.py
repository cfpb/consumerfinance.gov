import os
from pathlib import Path

from django.utils.encoding import force_str
from django.utils.text import slugify

import boto3

from agreements.models import Issuer


def s3_safe_key(path, prefix=''):
    key = prefix + path
    key = key.replace(' ', '_')
    key = key.replace('%', '')
    key = key.replace(';', '')
    key = key.replace(',', '')
    return key


def upload_to_s3(pdf_obj, s3_key):
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')

    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)

    s3_client.upload_fileobj(pdf_obj, AWS_STORAGE_BUCKET_NAME, s3_key)


def filename_in_zip(file_info):
    # Zip files default to IBM Code Page 437 encoding unless a specific bit
    # is set. See Appendix D in the zip file spec:
    # https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
    if (file_info.flag_bits & 0x800) == 0:
        return file_info.filename
    else:
        return force_str(file_info.filename, 'cp437')


def get_issuer(name):
    slug = slugify(name)
    try:
        issuer = Issuer.objects.get(slug=slug)
    except Issuer.DoesNotExist:
        issuer = Issuer(slug=slug, name=name)
        issuer.save()
    return issuer


def save_agreement(agreements_zip, pdf_path, outfile,
                   upload=False):
    uri_hostname = 'https://files.consumerfinance.gov'
    s3_prefix = 'a/assets/credit-card-agreements/pdf/'

    zipinfo = agreements_zip.getinfo(pdf_path)

    path = force_str(pdf_path)

    try:
        filename = Path(path).parts[-1]
        issuer_name = Path(path).parts[-2]
    except ValueError:
        # too many slashes...
        outfile.write("%s Does not match issuer/file.pdf pattern" % path)
        return

    issuer = get_issuer(issuer_name)
    s3_key = s3_safe_key(path, prefix=s3_prefix)

    agreement = issuer.agreement_set.create(
        file_name=filename,
        size=int(zipinfo.file_size),
        uri="{}/{}".format(uri_hostname, s3_key),
        description=filename)
    agreement.save()

    if upload:
        pdf_file = agreements_zip.open(zipinfo)
        upload_to_s3(pdf_file, s3_key)
        outfile.write(u'{} uploaded'.format(
            repr(s3_key),
        ))

    return agreement
