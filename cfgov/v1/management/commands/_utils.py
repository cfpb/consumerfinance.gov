import getpass

from django.contrib.auth import get_user_model
from django.test import Client

import input


class WagtailClient:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()

    def login(self):
        username = input('Wagtail username:')

        password = getpass.getpass(prompt='Wagtail password:')
        response = self.client.login(
            password=password,
            **{get_user_model().USERNAME_FIELD: username}
        )

        return response
