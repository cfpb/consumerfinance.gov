from datetime import timedelta
from itertools import chain

from django.conf import settings
from django.core.cache import cache, caches
from django.dispatch import receiver
from django.utils import timezone

from wagtail.core.signals import page_published, page_unpublished

from teachers_digital_platform.models.activity_index_page import (
    ActivityPage, ActivitySetUp
)
from v1.models import AbstractFilterPage, CFGOVPage
from v1.models.caching import AkamaiBackend
from v1.models.filterable_list_mixins import (
    CategoryFilterableMixin, FilterableListMixin
)
from v1.util.ref import get_category_children


def new_phi(user, expiration_days=90, locked_days=1):
    now = timezone.now()
    locked_until = now + timedelta(days=locked_days)
    expires_at = now + timedelta(days=expiration_days)

    from v1.models import PasswordHistoryItem
    password_history = PasswordHistoryItem(
        user=user,
        encrypted_password=user.password,
        locked_until=locked_until,
        expires_at=expires_at
    )

    password_history.save()
    user.temporarylockout_set.all().delete()


def user_save_callback(sender, **kwargs):
    user = kwargs['instance']

    if kwargs['created']:
        if user.is_superuser:
            # If a superuser was created, don't expire its password.
            new_phi(user, locked_days=0)
        else:
            # If a regular user was just created, force a new password to be
            # set right away by expiring the password and unlocking it.
            new_phi(user, locked_days=0, expiration_days=0)
    else:
        current_password_history = user.passwordhistoryitem_set.latest()
        if user.password != current_password_history.encrypted_password:
            new_phi(user)


def invalidate_post_preview(sender, **kwargs):
    instance = kwargs['instance']
    caches['post_preview'].delete(instance.post_preview_cache_key)


page_published.connect(invalidate_post_preview)


def invalidate_filterable_list_caches(sender, **kwargs):
    """ Invalidate filterable list caches when necessary

    When a filterable page is published or unpublished, we need to invalidate
    the caches related to the filterable list page that it might belong to.
    """
    page = kwargs['instance']

    # There's nothing to do if this page isn't a filterable page
    if not isinstance(page, AbstractFilterPage):
        return

    # Determine which filterable list page this page might belong
    # First, check to see if it has any ancestors that are
    # FilterableListMixins.
    filterable_list_pages = page.get_ancestors().type(
        FilterableListMixin
    ).specific().all()

    # Next, see if it belongs to any CategoryFilterableMixin filterable lists
    page_categories = page.categories.values_list('name', flat=True)
    category_filterable_list_pages = (
        category_filterable_list_page
        for category_filterable_list_page in CFGOVPage.objects.type(
            CategoryFilterableMixin
        ).specific()
        if any(
            category for category in page_categories
            if category in get_category_children(
                category_filterable_list_page.filterable_categories
            )
        )
    )

    # Combine parent filterable list pages and category filterable list pages
    filterable_list_pages = list(chain(
        filterable_list_pages,
        category_filterable_list_pages
    ))

    cache_tags_to_purge = []
    for filterable_list_page in filterable_list_pages:
        cache_key_prefix = filterable_list_page.get_cache_key_prefix()

        # Delete internal cache for the filterable list page
        cache.delete(f"{cache_key_prefix}-all_filterable_results")
        cache.delete(f"{cache_key_prefix}-page_ids")
        cache.delete(f"{cache_key_prefix}-topics")
        cache.delete(f"{cache_key_prefix}-authors")

        # Add the filterable list's slug to the list of cache tags to purge
        cache_tags_to_purge.append(filterable_list_page.slug)

    # Get the cache backend and purge filterable list page cache tags
    cache_backend = configure_akamai_backend()
    cache_backend.purge_by_tags(cache_tags_to_purge)


page_published.connect(invalidate_filterable_list_caches)
page_unpublished.connect(invalidate_filterable_list_caches)


def refresh_tdp_activity_cache():
    """Refresh the activity setups when a live ActivityPage is changed."""
    activity_setup = ActivitySetUp.objects.first()
    if not activity_setup:
        activity_setup = ActivitySetUp()
    activity_setup.update_setups()


def configure_akamai_backend():
    global_settings = getattr(settings, 'WAGTAILFRONTENDCACHE', {})
    akamai_settings = global_settings.get("akamai", {})
    akamai_params = {
        "CLIENT_TOKEN": akamai_settings.get("CLIENT_TOKEN", "test_token"),
        "CLIENT_SECRET": akamai_settings.get("CLIENT_SECRET", "test_secret"),
        "ACCESS_TOKEN": akamai_settings.get("ACCESS_TOKEN", "test_access"),
    }
    backend = AkamaiBackend(akamai_params)
    return backend


@receiver(page_published, sender=ActivityPage)
@receiver(page_unpublished, sender=ActivityPage)
def activity_published_handler(instance, **kwargs):
    refresh_tdp_activity_cache()
