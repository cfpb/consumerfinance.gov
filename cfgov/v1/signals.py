from datetime import timedelta

from django.core.cache import caches
from django.utils import timezone

from wagtail.core.signals import page_published


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
