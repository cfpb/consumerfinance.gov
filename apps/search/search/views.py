from django.shortcuts import render
from django.views.generic import View

from wagtail.core.models import get_page_models

from search.forms import ExternalLinksForm
from v1.models.resources import Resource
from v1.models.snippets import Contact, ReusableText


class SearchView(View):
    template_name = "search/external_links.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": ExternalLinksForm()}
        )

    def post(self, request):
        form = ExternalLinksForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        url = form.cleaned_data["url"]
        pages = []

        for cls in get_page_models():
            pages += list(cls.objects.search(url))

        pages = self.remove_duplicates(pages)
        pages = sorted(pages, key=lambda k: k.title)

        contacts = list(Contact.objects.filter(body__contains=url))
        resources = sorted(
            list(Resource.objects.filter(link__contains=url))
            + list(Resource.objects.filter(alternate_link__contains=url)),
            key=lambda k: k.title,
        )
        reusable_texts = list(
            ReusableText.objects.filter(text__contains=url).order_by("title")
        )

        num_page_results = len(pages)
        num_snippet_results = len(contacts + resources + reusable_texts)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "pages": pages,
                "contacts": contacts,
                "resources": resources,
                "reusable_texts": reusable_texts,
                "num_page_results": num_page_results,
                "num_snippet_results": num_snippet_results,
            },
        )

    @staticmethod
    def remove_duplicates(pages):
        seen = set()
        for page in pages:
            if page.pk not in seen:
                seen.add(page.pk)
                yield page
