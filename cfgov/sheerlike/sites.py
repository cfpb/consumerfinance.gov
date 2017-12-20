from django.conf import settings
from django.conf.urls import url
from django.views.generic.base import RedirectView

from unipath import Path

from sheerlike.views.generic import SheerTemplateView


class SheerSite(object):

    def __init__(self, slug):
        self.slug = slug
        if slug in settings.SHEER_SITES:
            self.path = Path(settings.SHEER_SITES[slug])
        else:
            self.path = None

    @property
    def urls(self):
        return self.urls_for_prefix()

    def urls_for_prefix(self, prefix='.'):
        url_patterns = []

        if self.path is None or not self.path.exists():
            return url_patterns

        prefixed_path = Path(self.path, prefix)
        for html_path in prefixed_path.walk():
            # skip files that don't end in .html
            if not html_path.endswith('.html'):
                continue
            rel_path = self.path.rel_path_to(html_path)
            prefix_rel_path = prefixed_path.rel_path_to(html_path)
            # skip files in underscore directories
            if rel_path.startswith('_'):
                continue
            view = SheerTemplateView.as_view(
                template_engine=self.slug,
                template_name=str(rel_path))
            regex_template = r'^%s$'
            index_template = r'^%s/$'
            if rel_path.name == 'index.html':
                if prefix_rel_path.parent:
                    slash_regex = index_template % prefix_rel_path.parent
                else:
                    slash_regex = r'^$'
                pattern = url(slash_regex, view)
                redirect_regex = regex_template % prefix_rel_path
                index_redirect = RedirectView.as_view(url='./', permanent=True)
                redirect_pattern = url(redirect_regex, index_redirect)
                url_patterns += [pattern, redirect_pattern]
            else:
                regex = regex_template % prefix_rel_path
                pattern = url(regex, view)
                url_patterns.append(pattern)
        return url_patterns
