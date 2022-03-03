import datetime
import logging

import django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone

from wagtail.contrib.frontend_cache.utils import PurgeBatch

from dateutil.relativedelta import relativedelta
from requests.exceptions import HTTPError

from v1.admin_forms import CacheInvalidationForm, ExportFeedbackForm
from v1.models.caching import AkamaiBackend, CDNHistory

try:
    from django.views.generic.edit import FormView
except ImportError:
    from django.views.generic import FormView


logger = logging.getLogger(__name__)


def cdn_is_configured():
    return (
        hasattr(settings, "WAGTAILFRONTENDCACHE")
        and settings.WAGTAILFRONTENDCACHE
    )


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
        return render(request, "cdnadmin/disabled.html")

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


class ExportFeedbackView(PermissionRequiredMixin, FormView):
    permission_required = "v1.export_feedback"
    template_name = "v1/export_feedback.html"
    form_class = ExportFeedbackForm

    def form_valid(self, form):
        # TODO: In Django 2.1, use as_attachment=True and pass the filename
        # as an argument instead of manually specifying the content headers.
        if django.VERSION > (2, 1):
            response = FileResponse(
                form.generate_zipfile(),
                as_attachment=True,
                content_type="application/zip",
            )
        else:
            response = FileResponse(
                form.generate_zipfile(), content_type="application/zip"
            )
        response[
            "Content-Disposition"
        ] = f"attachment;filename=feedback_{form.filename_dates}.zip"

        return response

    def get_initial(self):
        most_recent_quarter = self.get_most_recent_quarter()

        return {
            "from_date": most_recent_quarter[0],
            "to_date": most_recent_quarter[1],
        }

    @staticmethod
    def get_most_recent_quarter(today=None):
        """Returns the start and end date of the most recent quarter.

        For example, calling this method on 2019/12/01 would return
        (2019/07/01, 2019/09/30).
        """
        today = today or timezone.now().date()

        current_quarter_start = datetime.date(
            today.year, 1 + (((today.month - 1) // 3) * 3), 1
        )

        return (
            current_quarter_start - relativedelta(months=3),
            current_quarter_start - relativedelta(days=1),
        )
