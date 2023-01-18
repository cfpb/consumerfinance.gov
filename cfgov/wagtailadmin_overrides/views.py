from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from wagtail.admin.views.pages.utils import get_valid_next_url_from_request
from wagtail.models import Page


# This code was backported rom Wagtail 3.0 to support this feature:
#
# https://docs.wagtail.org/en/stable/releases/3.0.html#page-descriptions
#
# The original code lives at:
#
# https://github.com/wagtail/wagtail/blob/v2.15.5/wagtail/admin/views/pages/create.py#L21
#
# This code has been further modified to hide inherited page descriptions for
# derived page types who inherit from a page type that defines one. For
# example, if class FooPage defines a description, and class BarPage inherits
# from FooPage but does not define one, BarPage should not show FooPage's
# description.
def add_subpage(request, parent_page_id):
    parent_page = get_object_or_404(Page, id=parent_page_id).specific
    if not parent_page.permissions_for_user(request.user).can_add_subpage():
        raise PermissionDenied

    # Moved here from Page.get_page_description. This code needs to live on
    # the base page model in order for this view class to work with test
    # page model classes that may not inherit from our CFGOVPage.
    def get_page_description(cls):
        description = getattr(cls, "page_description", None)

        # Only show page descriptions defined on the specific page type.
        if "page_description" not in cls.__dict__:
            return ""

        # Make sure that page_description is actually a string rather than a
        # model field.
        if isinstance(description, str):
            return description
        elif getattr(description, "_delegate_text", None):
            # description is a lazy object (e.g. the result of gettext_lazy())
            return str(description)
        else:
            return ""

    page_types = [
        (
            model.get_verbose_name(),
            model._meta.app_label,
            model._meta.model_name,
            get_page_description(model),
        )
        for model in type(parent_page).creatable_subpage_models()
        if model.can_create_at(parent_page)
    ]
    # sort by lower-cased version of verbose name
    page_types.sort(key=lambda page_type: page_type[0].lower())

    if len(page_types) == 1:
        # Only one page type is available - redirect straight to the create
        # form rather than making the user choose.
        verbose_name, app_label, model_name, description = page_types[0]
        return redirect(
            "wagtailadmin_pages:add", app_label, model_name, parent_page.id
        )

    return TemplateResponse(
        request,
        "wagtailadmin/pages/add_subpage.html",
        {
            "parent_page": parent_page,
            "page_types": page_types,
            "next": get_valid_next_url_from_request(request),
        },
    )
