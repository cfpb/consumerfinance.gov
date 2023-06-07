import logging
import re
from functools import cached_property

from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.template import loader
from django.views.generic import ListView

from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.models import Site

from requests.exceptions import HTTPError

from v1.admin_forms import CacheInvalidationForm
from v1.models import AbstractFilterPage, CDNHistory
from v1.models.caching import AkamaiBackend


logger = logging.getLogger(__name__)


def cdn_is_configured():
    return bool(getattr(settings, "WAGTAILFRONTENDCACHE", None))


def purge(url=None):
    akamai_config = settings.WAGTAILFRONTENDCACHE.get("akamai", {})
    cloudfront_config = settings.WAGTAILFRONTENDCACHE.get("files", {})

    if url:
        # Use the Wagtail frontendcache PurgeBatch to perform the purge
        batch = PurgeBatch()
        batch.add_url(url)

        # If the URL matches any of our CloudFront distributions, invalidate
        # with that backend
        if any(
            k for k in cloudfront_config.get("DISTRIBUTION_ID", {}) if k in url
        ):
            logger.info('Purging {} from "files" cache'.format(url))
            batch.purge(backends=["files"])

        # Otherwise invalidate with our default backend
        else:
            logger.info('Purging {} from "akamai" cache'.format(url))
            batch.purge(backends=["akamai"])

        return "Submitted invalidation for %s" % url

    else:
        # purge_all only exists on our AkamaiBackend
        backend = AkamaiBackend(akamai_config)
        logger.info('Purging entire site from "akamai" cache')
        backend.purge_all()
        return "Submitted invalidation for the entire site."


def manage_cdn(request):
    if not cdn_is_configured():
        raise Http404

    user_can_purge = request.user.has_perm("v1.add_cdnhistory")

    if request.method == "GET":
        form = CacheInvalidationForm()

    elif request.method == "POST":
        if not user_can_purge:
            return HttpResponseForbidden()

        form = CacheInvalidationForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            history_item = CDNHistory(
                subject=url or "entire site", user=request.user
            )

            try:
                message = purge(url)
                history_item.message = message
                history_item.save()
                messages.success(request, message)
            except Exception as e:
                if isinstance(e, HTTPError):
                    error_info = e.response.json()
                    error_message = "{title}: {detail}".format(**error_info)
                else:
                    error_message = repr(e)

                history_item.message = error_message
                history_item.save()
                messages.error(request, error_message)

        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, "Error in %s: %s" % (field, error))

    history = CDNHistory.objects.all().order_by("-created")[:20]
    return render(
        request,
        "cdnadmin/index.html",
        context={
            "form": form,
            "user_can_purge": user_can_purge,
            "history": history,
        },
    )


class PagePreviewComparison(ListView):
    paginate_by = 100
    template_name = "v1/page_preview_comparison.html"

    def get_queryset(self):
        return (
            AbstractFilterPage.objects.in_site(
                Site.objects.get(is_default_site=True)
            )
            .prefetch_related("tags")
            .prefetch_related("categories")
            .order_by("title")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "render_snapshot": self.render_snapshot,
                "changes_alter_preview": self.changes_alter_preview,
            }
        )

        return context

    @cached_property
    def post_preview_snapshot(self):
        return loader.get_template("v1/includes/organisms/post-preview.html")

    def clean(self, s):
        s = re.sub(r"\s+", " ", s)
        s = re.sub(r' data-block-key="\w+"', "", s)
        return s

    def changes_alter_preview(self, page):
        html = self.render_snapshot(page)
        patched_html = self.render_snapshot(page, patch_fields=True)
        return self.clean(html) != self.clean(patched_html)

    def render_snapshot(self, page, patch_fields=False):
        # preview subheading, charfield
        # preview description, richtextfield

        old_preview_title = page.preview_title
        old_preview_subheading = page.preview_subheading
        old_preview_description = page.preview_description
        old_preview_image = page.preview_image

        if patch_fields:
            page.preview_title = page.seo_title
            page.preview_subheading = None
            page.preview_description = (
                f"<p>{page.search_description}</p>"
                if page.search_description
                else ""
            )
            page.preview_image = None

        html = self.post_preview_snapshot.template.module.render(
            post=page,
            controls={},
            show_date=False,
            show_tags=False,
        )

        if patch_fields:
            page.preview_title = old_preview_title
            page.preview_subheading = old_preview_subheading
            page.preview_description = old_preview_description
            page.preview_image = old_preview_image

        return html
