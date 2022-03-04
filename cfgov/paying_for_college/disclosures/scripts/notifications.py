import datetime
from string import Template

from django.core.mail import send_mail
from django.utils import timezone

from paying_for_college.models import Notification


INTRO = (
    "Notification failures \n"
    "Notification delivery failed for the following offer IDs:\n\n"
)
NOTE_TEMPLATE = Template(
    (
        "Offer ID $oid:\n"
        "    timestamp: $time\n"
        "    app errors: $errors\n"
        "SEND LOG:\n$log\n"
    )
)


def retry_notifications(days=1):
    """attempt to resend recent notifications that failed"""

    endmsg = ""
    days_old = timezone.now() - datetime.timedelta(days=int(days))
    failed_notifications = Notification.objects.filter(
        sent=False, timestamp__gt=days_old
    )
    for each in failed_notifications:
        endmsg += "{}\n".format(each.notify_school())
    if not endmsg:
        endmsg = "No failed notifications found"
    return endmsg


def send_stale_notifications(add_email=None):
    """Gather up notifications that have failed and are more than a day old."""

    if not add_email:
        add_email = []

    stale_date = timezone.now() - datetime.timedelta(days=1)
    stale_notifications = Notification.objects.filter(
        sent=False, timestamp__lt=stale_date
    )
    if not stale_notifications:
        return "No stale notifications found"
    contacts = {
        notification.institution.contact: []
        for notification in stale_notifications
        if notification.institution.contact
    }
    for noti in stale_notifications:
        payload = {
            "oid": noti.oid,
            "time": noti.timestamp.isoformat(),
            "errors": noti.errors,
            "log": noti.log,
        }
        clist = contacts[noti.institution.contact]
        clist.append(payload)
    for contact in contacts:
        msg = INTRO
        for msgdict in contacts[contact]:
            msg += NOTE_TEMPLATE.substitute(msgdict)
        recipients = contact.contacts.split(",") + add_email
        send_mail(
            "CFPB notification failures",
            msg,
            "no-reply@cfpb.gov",
            recipients,
            fail_silently=False,
        )
        return "Found {} stale notifications; emails sent to " "{}".format(
            stale_notifications.count(), recipients
        )
