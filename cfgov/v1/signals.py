import json

from datetime import timedelta
from django.dispatch import Signal
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from wagtail.wagtailcore.signals import page_published, page_unpublished


page_unshared = Signal(providing_args=['instance'])


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


# Sets all the revisions for a page's attribute to False when it's called
def update_all_revisions(instance, attr):
    for revision in instance.revisions.all():
        content = json.loads(revision.content_json)
        if content[attr]:
            content[attr] = False
            revision.content_json = unicode(json.dumps(content), 'utf-8')
            revision.save()


def unshare_all_revisions(sender, **kwargs):
    from v1.wagtail_hooks import flush_akamai
    update_all_revisions(kwargs['instance'], 'shared')
    flush_akamai(page=kwargs['instance'])


def unpublish_all_revisions(sender, **kwargs):
    from v1.wagtail_hooks import flush_akamai
    update_all_revisions(kwargs['instance'], 'live')
    flush_akamai(page=kwargs['instance'])


def configure_page_and_revision(sender, **kwargs):
    from v1.wagtail_hooks import share, configure_page_revision, flush_akamai
    share(page=kwargs['instance'], is_sharing=False, is_live=True)
    configure_page_revision(page=kwargs['instance'], is_sharing=False, is_live=True)
    flush_akamai(page=kwargs['instance'])


page_unshared.connect(unshare_all_revisions)
page_unpublished.connect(unpublish_all_revisions)
page_published.connect(configure_page_and_revision)
