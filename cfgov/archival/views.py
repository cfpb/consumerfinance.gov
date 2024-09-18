from io import BytesIO

from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from wagtail.models import Page

from archival.forms import ImportForm
from archival.utils import export_page, import_page


def export_view(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    page_json = export_page(page)
    page_io = BytesIO(page_json.encode())
    response = FileResponse(
        page_io,
        as_attachment=True,
        filename=f"{page.slug}.json",
    )
    return response


def import_view(request, page_id):
    parent_page = get_object_or_404(Page, id=page_id).specific

    if request.method == "POST":
        input_form = ImportForm(request.POST, request.FILES)

        if input_form.is_valid():
            json_file = request.FILES["page_file"]
            try:
                new_page = import_page(
                    parent_page, json_file.read().decode("utf8")
                )
            except Exception:
                input_form.add_error(
                    "page_file",
                    "There was an error importing this file as a page. "
                    "Please ensure the app and model it references exist, "
                    "and that its schema is up to date.",
                )
            else:
                return redirect("wagtailadmin_pages:edit", new_page.id)
    else:
        input_form = ImportForm()

    return TemplateResponse(
        request,
        "archival/import_page.html",
        {
            "parent_page": parent_page,
            "form": input_form,
        },
    )
