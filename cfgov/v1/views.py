from core.services import PDFGeneratorView, ICSView


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
