from __future__ import unicode_literals

import json
from six import text_type as unicode
from six.moves.urllib.parse import urljoin

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from haystack.inputs import Clean
from haystack.query import SearchQuerySet

from wagtail.wagtailcore.models import Site
from wagtailsharing.models import SharingSite
from wagtailsharing.views import ServeView

from bs4 import BeautifulSoup as bs
from flags.state import flag_enabled

from ask_cfpb.models import Answer, AnswerPage, AnswerResultsPage


def annotate_links(answer_text):
    """
    Parse and annotate links from answer text and return the annotated answer
    and an enumerated list of links as footnotes.
    """

    try:
        SITE = Site.objects.get(is_default_site=True)
    except Site.DoesNotExist:
        raise RuntimeError('no default wagtail site configured')

    footnotes = []
    soup = bs(answer_text, 'lxml')
    links = soup.findAll('a')
    index = 1
    for link in links:
        if not link.get('href'):
            continue
        footnotes.append(
            (index, urljoin(SITE.root_url, link.get('href'))))
        parent = link.parent
        link_location = parent.index(link)
        super_tag = soup.new_tag('sup')
        super_tag.string = str(index)
        parent.insert(link_location + 1, super_tag)
        index += 1
    return (unicode(soup), footnotes)


def print_answer(request, slug, language, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    field_map = {
        'es': {'slug': answer.slug_es,
               'title': answer.question_es,
               'answer_text': answer.answer_es},
        'en': {'slug': answer.slug,
               'title': answer.question,
               'answer_text': answer.answer},
    }
    _map = field_map[language]
    if not _map['answer_text']:
        raise Http404
    (text, footnotes) = annotate_links(_map['answer_text'])

    print_context = {
        'answer': text,
        'title': _map['title'],
        'slug': _map['slug'],
        'footnotes': footnotes
    }
    return render(
        request,
        'ask-cfpb/answer-page-spanish-printable.html',
        context=print_context)


def view_answer(request, slug, language, answer_id):
    answer_page = get_object_or_404(
        AnswerPage, language=language, answer_base__id=answer_id)
    if answer_page.live is False:
        raise Http404
    if answer_page.redirect_to_page:
        new_page = answer_page.redirect_to_page
        return redirect(new_page.url, permanent=True)
    if "{}-{}-{}".format(slug, language, answer_id) != answer_page.slug:
        return redirect(answer_page.url, permanent=True)
    else:
        try:
            sharing_site = SharingSite.find_for_request(request)
        except SharingSite.DoesNotExist:
            return answer_page.serve(request)
        page, args, kwargs = ServeView.get_requested_page(
            sharing_site.site,
            request,
            request.path)
        return ServeView.serve_latest_revision(
            page, request, args, kwargs)


def ask_search(request, language='en', as_json=False):
    if 'selected_facets' in request.GET:
        return redirect_ask_search(request, language=language)
    language_map = {
        'en': 'ask-cfpb-search-results',
        'es': 'respuestas'
    }
    sqs = SearchQuerySet().models(AnswerPage)
    clean_query = Clean(request.GET.get('q', ''))
    clean_qstring = clean_query.query_string.strip()
    qstring = clean_qstring
    query_sqs = sqs.filter(
        content=clean_query,
        language=language
    )
    results_page = get_object_or_404(
        AnswerResultsPage,
        language=language,
        slug=language_map[language]
    )

    # If there's no query string, don't search
    if not qstring:
        results_page.query = ''
        results_page.result_query = ''
        return results_page.serve(request)

    # If we have no results from our query, let's try to suggest a better one
    suggestion = sqs.spelling_suggestion(qstring)
    if suggestion == qstring:
        suggestion = None
    elif (query_sqs.count() == 0 and
            request.GET.get('correct', '1') == '1' and
            flag_enabled('ASK_SEARCH_TYPOS', request=request)):
        query_sqs = sqs.filter(content=suggestion)
        qstring, suggestion = suggestion, qstring

    if as_json:
        results = {
            'query': clean_qstring,
            'result_query': qstring,
            'suggestion': suggestion,
            'results': [
                {
                    'question': result.autocomplete,
                    'url': result.url,
                    'text': result.text
                }
                for result in query_sqs
            ]
        }
        json_results = json.dumps(results)
        return HttpResponse(json_results, content_type='application/json')
    else:
        results_page.query = clean_qstring
        results_page.result_query = qstring
        results_page.suggestion = suggestion
        results_page.answers = []

        for result in query_sqs:
            results_page.answers.append(
                (result.url, result.autocomplete, result.text)
            )
        return results_page.serve(request)


def ask_autocomplete(request, language='en'):
    term = request.GET.get(
        'term', '').strip().replace('<', '')
    if not term:
        return JsonResponse([], safe=False)
    sqs = SearchQuerySet().models(AnswerPage)
    sqs = sqs.autocomplete(
        autocomplete=term,
        language=language
    )
    results = [{'question': result.autocomplete,
                'url': result.url}
               for result in sqs[:20]]
    return JsonResponse(results, safe=False)


def redirect_ask_search(request, language='en'):
    """
    Catch old pages built via query string and
    redirect them to category pages if we can. If the query string
    has a 'q' query, we'll run that search. Otherwise, we look for faceting.

    We want to catch these search facets, in this order:
    - selected_facets=category_exact:
    - selected_facets=audience_exact
    - selected_facets=tag_exact:
    """

    category_facet = 'category_exact:'
    audience_facet = 'audience_exact:'
    tag_facet = 'tag_exact:'
    if request.GET.get('q'):
        querystring = request.GET.get('q').strip()
        if not querystring:
            raise Http404
        return redirect(
            '/ask-cfpb/search/?q={query}'.format(
                query=querystring, permanent=True))
    else:
        facets = request.GET.getlist('selected_facets')
        if not facets or not facets[0]:
            raise Http404

        def redirect_to_category(category, language):
            if language == 'es':
                return redirect(
                    '/es/obtener-respuestas/categoria-{category}/'.format(
                        category=category), permanent=True)
            return redirect(
                '/ask-cfpb/category-{category}/'.format(
                    category=category), permanent=True)

        def redirect_to_audience(audience):
            """We currently only offer audience pages to English users"""
            return redirect(
                '/ask-cfpb/audience-{audience}/'.format(
                    audience=audience), permanent=True)

        def redirect_to_tag(tag, language):
            """for URLs, tags are passed with words separated by underscores"""
            if language == 'es':
                return redirect(
                    '/es/obtener-respuestas/buscar-por-etiqueta/{tag}/'.format(
                        tag=tag), permanent=True)
            else:
                return redirect(
                    '/ask-cfpb/search-by-tag/{tag}/'.format(
                        tag=tag), permanent=True)

        # Redirect by facet value, if there is one, starting with category.
        # We want to exhaust facets each time, so we need three loops.
        # We act only on the first of any facet type found.
        # Most search redirects will find a category and return.
        for facet in facets:
            if category_facet in facet:
                category = facet.replace(category_facet, '')
                if category:
                    return redirect_to_category(category, language)

        for facet in facets:
            if audience_facet in facet:
                audience_raw = facet.replace(audience_facet, '')
                if audience_raw:
                    audience = slugify(audience_raw.replace('+', '-'))
                    return redirect_to_audience(audience)

        for facet in facets:
            if tag_facet in facet:
                raw_tag = facet.replace(tag_facet, '')
                if raw_tag:
                    tag = raw_tag.replace(
                        ' ', '_').replace(
                        '%20', '_').replace(
                        '+', '_')
                    return redirect_to_tag(tag, language)

        raise Http404
