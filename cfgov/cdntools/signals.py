import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.documents.models import Document


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Document)
def cloudfront_cache_invalidation(sender, instance, **kwargs):
    if not settings.ENABLE_CLOUDFRONT_CACHE_PURGE:
        return

    if not instance.file:
        return

    url = instance.file.url

    logger.info(f'Purging {url} from "files" cache')

    batch = PurgeBatch()
    batch.add_url(url)
    batch.purge(backends=["files"])
