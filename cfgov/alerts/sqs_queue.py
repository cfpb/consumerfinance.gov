import boto3


class SQSQueue:
    def __init__(self, queue_url, client=None, credentials=None):
        if not credentials:
            credentials = {}
        self.queue_url = queue_url
        self.client = client or self.get_client(credentials)

    def get_client(self, credentials):
        return boto3.client(
            "sqs",
            aws_access_key_id=credentials.get("access_key"),
            aws_secret_access_key=credentials.get("secret_key"),
            region_name=credentials.get("region_name", "us-east-1"),
        )

    def post(self, message):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message,
        )
        return response
