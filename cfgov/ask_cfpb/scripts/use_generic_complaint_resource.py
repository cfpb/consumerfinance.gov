from __future__ import unicode_literals

import datetime
import os

from django.contrib.auth.models import User

from v1.models.snippets import RelatedResource


GENERIC_PK = 18  # The generic "Submit a complaint" related resource
UNWANTED_RESOURCE_PKS = {
    1: 'Credit reporting complaint',
    15: 'Payday loan complaint',
    16: 'Money transfers complaint',
    17: 'Debt collection complaint',
    19: 'Auto loan complaint',
    20: 'Submit a bank account complaint',
    21: 'Vehicle or consumer loan complaint',
    22: 'Student loan complaint',
    23: 'Mortgage complaint',
    24: 'Submit a credit card complaint'
}


def replace_complaint_resources():
    """Replace all related-resource complaint links with generic resource."""
    start = datetime.datetime.now()
    count = 0
    migration_user_pk = os.getenv('MIGRATION_USER_PK', 9999)
    user = User.objects.filter(id=migration_user_pk).first()
    for unwanted_pk in UNWANTED_RESOURCE_PKS:
        resource = RelatedResource.objects.get(pk=unwanted_pk)
        for page in resource.answerpage_set.exclude(pk=GENERIC_PK):
            count += 1
            draft = page.status_string == 'draft'
            page.get_latest_revision().publish()
            page.related_resource_id = GENERIC_PK
            page.save_revision(user=user).publish()
            if draft:
                page.unpublish()
    return (
        "Converted {} pages to use the generic complaint resource.\n"
        "The script took {} to run.".format(
            count, (datetime.datetime.now() - start)))


def delete_unwanted():
    """
    To be run only after Ask pages have been converted to the generic snippet.

    Use the following Django shell command to delete unwanted resources:
    runscript use_generic_complaint_resource --script-args delete-unwanted
    """
    for pk, label in UNWANTED_RESOURCE_PKS.items():
        print("Deleting {}".format(label))
        RelatedResource.objects.get(pk=pk).delete()


def run(*args):
    if args:
        if args[0] == 'delete-unwanted':
            delete_unwanted()
    else:
        print(replace_complaint_resources())
