import json
from urllib.parse import urljoin

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify

from wagtail.core.models import Site
from wagtailsharing.models import SharingSite
from wagtailsharing.views import ServeView

from bs4 import BeautifulSoup as bs

from ask_cfpb.forms import AutocompleteForm, SearchForm, legacy_facet_validator
from ask_cfpb.models import AnswerPage, AnswerPageSearch, AnswerResultsPage


def annotate_links(answer_text):
    """
    Parse and annotate links from answer text.

    Return the annotated answer
    and an enumerated list of links as footnotes.
    """
    try:
        _site = Site.objects.get(is_default_site=True)
    except Site.DoesNotExist:
        raise RuntimeError("no default wagtail site configured")

    footnotes = []
    soup = bs(answer_text, "lxml")
    links = soup.findAll("a")
    index = 1
    for link in links:
        if not link.get("href"):
            continue
        footnotes.append((index, urljoin(_site.root_url, link.get("href"))))
        parent = link.parent
        link_location = parent.index(link)
        super_tag = soup.new_tag("sup")
        super_tag.string = str(index)
        parent.insert(link_location + 1, super_tag)
        index += 1
    return (str(soup), footnotes)


def view_answer(request, slug, language, answer_id):
    answer_page = get_object_or_404(
        AnswerPage, language=language, answer_base__id=answer_id
    )
    # We can't call answer_page.serve(request) yet because that would bypass
    # wagtail-sharing, which provides views of unpublished revisions.
    # First, we see if a sharing site is present in the request:
    try:
        sharing_site = SharingSite.find_for_request(request)
    except SharingSite.DoesNotExist:
        sharing_site = None
    # handle draft pages first
    if answer_page.live is False:
        if sharing_site is None:
            raise Http404
        else:
            return ServeView.serve(answer_page, request, [], {})
    # page is live
    # redirect if so configured
    if answer_page.redirect_to_page:
        new_page = answer_page.redirect_to_page
        return redirect(new_page.url, permanent=True)
    # handle pages that have unpublished revisions
    if answer_page.status_string == "live + draft":
        if sharing_site:
            return ServeView.serve(answer_page, request, [], {})
        else:
            return answer_page.serve(request)
    # page is live with no revisions. heal the URL if necessary
    if f"{slug}-{language}-{answer_id}" != answer_page.slug:
        return redirect(answer_page.url, permanent=True)

    return answer_page.serve(request)


def ask_search(request, language="en", as_json=False):
    if "selected_facets" in request.GET:
        return redirect_ask_search(request, language=language)

    search_form = SearchForm(request.GET, initial={"q": "", "correct": True})

    language_map = {"en": "ask-cfpb-search-results", "es": "respuestas"}
    results_page = get_object_or_404(
        AnswerResultsPage, language=language, slug=language_map[language]
    )

    # If there's no query string, don't search
    if not search_form.is_valid():
        results_page.query = ""
        results_page.result_query = ""
        return results_page.serve(request)

    search_term = search_form.cleaned_data["q"]
    page = AnswerPageSearch(search_term, language=language)
    response = page.search()

    # Check if we want to use the suggestion or not
    suggest = search_form.cleaned_data["correct"]

    # Provide a suggestion only when no results are found
    if not response.get("results") and suggest:
        response = page.suggest()
        suggestion = response.get("suggestion")
    else:
        suggestion = search_term

    if as_json:
        payload = {
            "query": search_term,
            "result_query": search_term.strip(),
            "suggestion": suggestion.strip(),
            "results": [
                {
                    "question": result.autocomplete,
                    "url": result.url,
                    "text": result.text,
                    "preview": result.preview,
                }
                for result in response.get("results")
            ],
        }
        json_results = json.dumps(payload)
        return HttpResponse(json_results, content_type="application/json")

    results_page.query = search_term
    results_page.result_query = response.get("search_term")
    results_page.suggestion = response.get("suggestion")
    results_page.answers = [
        (result.url, result.autocomplete, result.preview)
        for result in response["results"]
    ]
    return results_page.serve(request)


def ask_autocomplete(request, language="en"):
    autocomplete_form = AutocompleteForm(request.GET)

    if not autocomplete_form.is_valid():
        return JsonResponse([], safe=False)

    term = autocomplete_form.cleaned_data["term"]
    try:
        results = AnswerPageSearch(
            search_term=term, language=language
        ).autocomplete()
        return JsonResponse(results, safe=False)
    except IndexError:
        return JsonResponse([], safe=False)


def redirect_ask_search(request, language="en"):
    """
    Redirect legacy knowledgebase requests built via query strings.

    Prior to 2016, Ask CFPB (knowledgebase) built category, audience and
    search-tag pages based on query string facets. When Ask was migrated
    to Wagtail, we simplified the page structure and left this view
    to route legacy requests using the old query string faceting routine.

    Knowledgebase used /askcfpb/ (no hyphen) as its base URL node.

    If the legacy query string has no 'q' element or a blank one, we return
    the current base /ask-cfpb/search/ page.
    If the query string has a 'q' query, we'll run that search.
    Otherwise, we look for legacy faceting.

    We want to catch these search facets, in this order:
    - selected_facets=category_exact:
    - selected_facets=audience_exact
    - selected_facets=tag_exact:
    """
    category_facet = "category_exact:"
    audience_facet = "audience_exact:"
    tag_facet = "tag_exact:"

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data["q"]
        return redirect(f"/ask-cfpb/search/?q={query}", permanent=True)
    else:
        facets = request.GET.getlist("selected_facets")

        if not facets or not facets[0]:
            return redirect("/ask-cfpb/search/", permanent=True)

        try:
            for facet in facets:
                legacy_facet_validator(facets)
        except ValidationError:
            raise Http404

        def redirect_to_category(category, language):
            if language == "es":
                return redirect(
                    f"/es/obtener-respuestas/categoria-{category}/",
                    permanent=True,
                )
            return redirect(f"/ask-cfpb/category-{category}/", permanent=True)

        def redirect_to_audience(audience):
            """We currently only offer audience pages to English users."""
            return redirect(f"/ask-cfpb/audience-{audience}/", permanent=True)

        def redirect_to_tag(tag, language):
            """Handle tags passed with underscore separators."""
            if language == "es":
                return redirect(
                    f"/es/obtener-respuestas/buscar-por-etiqueta/{tag}/",
                    permanent=True,
                )
            else:
                return redirect(
                    f"/ask-cfpb/search-by-tag/{tag}/", permanent=True
                )

        # Redirect by facet value, if there is one, starting with category.
        # We want to exhaust facets each time, so we need three loops.
        # We act only on the first of any facet type found.
        # Most search redirects will find a category and return.
        for facet in facets:
            if category_facet in facet:
                category = facet.replace(category_facet, "")
                if category:
                    slug = slugify(category)  # handle uppercase and spaces
                    return redirect_to_category(slug, language)

        for facet in facets:
            if audience_facet in facet:
                audience_raw = facet.replace(audience_facet, "")
                if audience_raw:
                    audience = slugify(audience_raw.replace("+", "-"))
                    return redirect_to_audience(audience)

        for facet in facets:
            if tag_facet in facet:
                raw_tag = facet.replace(tag_facet, "")
                if raw_tag:
                    tag = (
                        raw_tag.replace(" ", "_")
                        .replace("%20", "_")
                        .replace("+", "_")
                    )
                    return redirect_to_tag(tag, language)

        raise Http404
