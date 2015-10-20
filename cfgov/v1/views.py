from core.services import PDFGeneratorView, ICSView
from wagtail.wagtailcore.models import Page
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from wagtail.wagtailadmin import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse


class LeadershipCalendarPDFView(PDFGeneratorView):
    render_url = 'http://localhost/the-bureau/leadership-calendar/print/'
    stylesheet_url = 'http://localhost/static/css/pdfreactor-fonts.css'
    filename = 'cfpb_leadership-calendar.pdf'


class EventICSView(ICSView):
    """
    View for ICS generation in the /events/ section
    """
    # Constants
    event_calendar_prodid = '-//CFPB//Event Calendar//EN',
    event_source = 'http://localhost:9200/content/events/<event_slug>/_source'

    # JSON key names
    event_summary_keyname = 'summary'
    event_dtstart_keyname = 'dtstart'
    event_dtend_keyname = 'dtend'
    event_dtstamp_keyname = 'dtstamp'
    event_uid_keyname = 'uid'
    event_priority_keyname = 'priority'
    event_organizer_keyname = 'organizer'
    event_organizer_addr_keyname = 'organizer_email'
    event_location_keyname = 'location'
    event_status_keyname = 'status'


def renderDirectoryPDF(request):
    pdf = open(settings.V1_TEMPLATE_ROOT + '/the-bureau/about-director/201410_cfpb_bio_cordray.pdf', 'rb').read()

    return HttpResponse(pdf, content_type='application/pdf')


def unshare(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    if not page.permissions_for_user(request.user).can_unshare():
        raise PermissionDenied

    if request.method == 'POST':
        page.shared = False
        page.save_revision(user=request.user, submitted_for_moderation=False)
        page.save()

        messages.success(request, _("Page '{0}' unshared.").format(page.title), buttons=[
            messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
        ])

        return redirect('wagtailadmin_explore', page.get_parent().id)

    return render(request, 'wagtailadmin/pages/confirm_unshare.html', {
        'page': page,
    })
