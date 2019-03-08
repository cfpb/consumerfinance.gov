# from django.core.paginator import InvalidPage, Paginator

from wagtail.wagtailcore.models import PageManager

from forms import HmdaFilterableForm
from hmda.resources.hmda_data_files import get_data_files
from hmda.resources.hmda_data_options import (
    HMDA_FIELD_DESC_OPTIONS, HMDA_GEO_OPTIONS, HMDA_RECORDS_OPTIONS
)

from v1.models import BrowsePage


class HmdaExplorerPage(BrowsePage):
    """
    A model for the new HMDA explorer page that displays links to S3 files
    containing HMDA data.
    """

    objects = PageManager()
    template = 'hmda/hmda-explorer.html'

    def get_context(self, request, *args, **kwargs):
        context = super(HmdaExplorerPage, self).get_context(
            request, *args, **kwargs)

        params = request.GET
        geo = params.get('geo', 'nationwide')
        labels = params.get('field_descriptions', 'labels')
        record_set = params.get('records', 'first-lien-owner-occupied-1-4-family-records')

        context.update({
            'form': HmdaFilterableForm(params),
            'title': self.get_title(geo, record_set),
            'files': get_data_files(geo, labels, record_set),
        })

        return context

    # TODO: refine the wording for these titles with designer input
    def get_title(self, location, record_set):
        location_name = dict(HMDA_GEO_OPTIONS).get(location, "State")
        records_name = dict(HMDA_RECORDS_OPTIONS).get(record_set, "records")
        return "{} records for {}".format(location_name, records_name)
