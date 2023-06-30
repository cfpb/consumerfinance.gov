from django.conf import settings

import boto3
from botocore.exceptions import (
    ClientError,
    ConnectionError,
    NoCredentialsError,
    ParamValidationError,
)


class Metadata:
    def __init__(self):
        s3 = boto3.resource("s3")
        self.bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME or "")
        self.prefix = "a/assets/bulk_agreements/"
        self.flexibilities = [
            "Q1-2020",
            "Q2-2020",
            "Q3-2020",
            "Q4-2020",
            "Q1-2021",
        ]
        self.notes = {
            "Q2-2019": "Agreements are incomplete due to technical submission"
            " issues at the Bureau"
        }

    def get_objects_by_prefix(self):
        return self.bucket.objects.filter(Prefix=self.prefix)

    def get_sorted_agreements(self, reverse=True):
        try:
            agreements = [f.key for f in self.get_objects_by_prefix()]
            agreements.sort(reverse=reverse)
            return agreements
        except (
            ClientError,
            ConnectionError,
            NoCredentialsError,
            ParamValidationError,
        ):
            return []
