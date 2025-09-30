import json
import logging

from django.core.exceptions import ImproperlyConfigured

from wagtail.contrib.frontend_cache.backends import BaseBackend

import requests
from akamai.edgegrid import EdgeGridAuth


logger = logging.getLogger(__name__)


class AkamaiBackend(BaseBackend):
    """Akamai backend that performs an 'invalidate' purge"""

    def __init__(self, params):
        super().__init__(params)
        self.client_token = params.get("CLIENT_TOKEN")
        self.client_secret = params.get("CLIENT_SECRET")
        self.access_token = params.get("ACCESS_TOKEN")
        self.object_id = params.get("OBJECT_ID")
        self.purge_all_url = params.get("PURGE_ALL_URL")
        self.fast_purge_url = params.get("FAST_PURGE_URL")
        if not all(
            (
                self.client_token,
                self.client_secret,
                self.access_token,
                self.object_id,
                self.purge_all_url,
                self.fast_purge_url,
            )
        ):
            raise ImproperlyConfigured(
                "Akamai CLIENT_TOKEN, CLIENT_SECRET, ACCESS_TOKEN, "
                "OBJECT_ID, PURGE_ALL_URL, and FAST_PURGE_URL "
                "must be configured."
            )
        self.auth = self.get_auth()
        self.headers = {"content-type": "application/json"}

    def get_auth(self):
        return EdgeGridAuth(
            client_token=self.client_token,
            client_secret=self.client_secret,
            access_token=self.access_token,
        )

    def get_payload(self, obj, action):
        return {"action": action, "objects": [obj]}

    def post_all(self, action):
        obj = self.object_id
        resp = requests.post(
            self.purge_all_url,
            headers=self.headers,
            data=json.dumps(self.get_payload(obj=obj, action=action)),
            auth=self.auth,
        )
        logger.info(
            f"Attempted to {action} content provider {obj}, "
            f"got back response {resp.text}"
        )
        resp.raise_for_status()

    def post(self, url, action):
        resp = requests.post(
            self.fast_purge_url,
            headers=self.headers,
            data=json.dumps(self.get_payload(obj=url, action=action)),
            auth=self.auth,
        )
        logger.info(
            f"Attempted to {action} cache for page {url}, "
            f"got back response {resp.text}"
        )
        resp.raise_for_status()

    def post_tags(self, tags, action):
        """Request a purge by cache_tags."""
        url = self.fast_purge_url.replace("url", "tag")
        resp = requests.post(
            url,
            headers=self.headers,
            data=json.dumps({"action": action, "objects": tags}),
            auth=self.auth,
        )
        logger.info(
            f"Attempted to {action} by cache_tags {', '.join(tags)}, "
            f"and got back the response {resp.text}"
        )
        resp.raise_for_status()

    def purge_by_tags(self, tags, action="invalidate"):
        self.post_tags(tags, action=action)

    def purge(self, url):
        self.post(url, "invalidate")

    def purge_all(self):
        self.post_all("invalidate")


class AkamaiDeletingBackend(AkamaiBackend):
    """Akamai backend that performs a 'delete' purge

    This is a special-case backend, and should not be globally configured."""

    def purge(self, url):
        self.post(url, "delete")

    def purge_all(self):
        raise NotImplementedError(
            "Purging all by deletion is intentionally not supported through "
            "this backend. Please use the Akamai Control Center."
        )


# This global will hold URLs that were purged by the MockAkamaiBackend for
# inspection.
MOCK_PURGED = []


class MockBackend(BaseBackend):
    def __init__(self, params):
        super().__init__(params)

    def purge(self, url):
        MOCK_PURGED.append(url)


class MockAkamaiBackend(BaseBackend):
    def __init__(self, params):
        super().__init__(params)

    def purge(self, url):
        MOCK_PURGED.append(url)

    def purge_all(self):
        MOCK_PURGED.append("__all__")

    def purge_by_tags(self, tags, **kwargs):
        MOCK_PURGED.extend(tags)
