from wagtail.core.models import PageManager

from hmda.models.forms import HmdaFilterableForm
from hmda.resources.hmda_data_options import (
    HMDA_FIELD_DESC_OPTIONS,
    HMDA_GEO_OPTIONS,
    HMDA_RECORDS_OPTIONS,
)
from hmda.resources.loan_file_metadata import LOAN_FILE_METADATA
from v1.models import LearnPage


class HmdaHistoricDataPage(LearnPage):
    """
    A model for the new HMDA Historic Data page that displays links to S3 files
    containing HMDA data.
    """

    objects = PageManager()
    template = "hmda/hmda-explorer.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        form_data = self.form_data(request.GET)
        plain_language_records = dict(HMDA_RECORDS_OPTIONS).get(
            form_data.get("records")
        )

        context.update(
            {
                "form": HmdaFilterableForm(form_data),
                "title": self.get_title(form_data.get("geo")),
                "subtitle": plain_language_records,
                "files": self.get_data_files(**form_data),
            }
        )

        return context

    def form_data(self, params):
        geo = self.value_or_default(HMDA_GEO_OPTIONS, params.get("geo"))
        labels = self.value_or_default(
            HMDA_FIELD_DESC_OPTIONS, params.get("field_descriptions")
        )
        record_set = self.value_or_default(HMDA_RECORDS_OPTIONS, params.get("records"))

        data = {
            "geo": geo,
            "field_descriptions": labels,
            "records": record_set,
        }
        return data

    def get_title(self, geo):
        if geo == "nationwide":
            return "Showing nationwide records"
        else:
            location_name = dict(HMDA_GEO_OPTIONS).get(geo, "State")
            return "Showing records for {}".format(location_name)

    def value_or_default(self, options, user_input):
        options_dict = dict(options)
        if user_input in options_dict:
            return user_input
        else:
            return options[0][0]

    def get_data_files(self, geo, field_descriptions, records):
        files = LOAN_FILE_METADATA[geo][field_descriptions][records]

        # sort files in reverse chronological order
        return sorted(files.items(), key=lambda t: t[0], reverse=True)
