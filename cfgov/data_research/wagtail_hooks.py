from wagtail.snippets.models import register_snippet

from data_research.views import DataResearchViewSetGroup


register_snippet(DataResearchViewSetGroup)
