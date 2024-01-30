from wagtail.snippets.models import register_snippet

from jobmanager import template_debug
from jobmanager.views import JobListingsViewSetGroup
from v1.template_debug import register_template_debug


register_snippet(JobListingsViewSetGroup)


for _debug_template_name in (
    "job_listing_details",
    "job_listing_list",
    "job_listing_table",
):
    register_template_debug(
        "jobmanager",
        _debug_template_name,
        f"jobmanager/{_debug_template_name}.html",
        getattr(template_debug, f"{_debug_template_name}_test_cases"),
    )
