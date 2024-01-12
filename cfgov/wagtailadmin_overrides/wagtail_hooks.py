from wagtail.snippets.models import register_snippet

from wagtailadmin_overrides.views import SnippetsViewSetGroup


register_snippet(SnippetsViewSetGroup)
