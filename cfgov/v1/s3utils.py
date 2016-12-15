"""Custom S3 storage backends to store files in subfolders."""
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

MediaRootS3BotoStorage = lambda: S3BotoStorage(location=settings.AWS_S3_ROOT)
