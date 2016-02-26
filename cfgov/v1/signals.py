import json

from datetime import timedelta

from django.dispatch import Signal
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from wagtail.wagtailcore.signals import page_unpublished

page_unshared = Signal(providing_args=['instance'])


def new_phi(user):

    from .models import PasswordHistoryItem

    now = timezone.now()
    locked_until = now + timedelta(days=1)
    expires_at = now + timedelta(days=90)

    password_history = PasswordHistoryItem(user=user,
            encrypted_password=user.password,
            locked_until = locked_until,
            expires_at = expires_at)

    password_history.save()
    user.temporarylockout_set.all().delete()

def user_save_callback(sender, **kwargs):
    user = kwargs['instance']    

    try:
        current_password_data = user.passwordhistoryitem_set.latest()
    
        if user.password != current_password_data.encrypted_password:
            new_phi(user)

    except ObjectDoesNotExist:
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
    update_all_revisions(kwargs['instance'], 'shared')

def unpublish_all_revisions(sender, **kwargs):
    update_all_revisions(kwargs['instance'], 'live')


page_unshared.connect(unshare_all_revisions)
page_unpublished.connect(unpublish_all_revisions)
