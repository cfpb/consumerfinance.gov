from __future__ import unicode_literals
import json
# import re
from urlparse import urljoin

from bs4 import BeautifulSoup as bs
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404, JsonResponse
from haystack.query import SearchQuerySet
from haystack.inputs import Clean
from wagtail.wagtailcore.models import Site

from ask_cfpb.models import (
    Answer,
    AnswerPage,
    AnswerResultsPage,
    EnglishAnswerProxy,
    SpanishAnswerProxy)


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
    if answer_page.redirect_to:
        new_page = answer_page.redirect_to.answer_pages.get(language=language)
        return redirect(new_page.url)
    if "{}-{}-{}".format(slug, language, answer_id) != answer_page.slug:
        return redirect(answer_page.url)
    else:
        return answer_page.serve(request)


def ask_search(request, language='en', as_json=False):
    if 'selected_facets' in request.GET:
        return redirect_ask_search(request, language=language)
    language_map = {
        'en': {'slug': 'ask-cfpb-search-results',
               'query': SearchQuerySet().models(EnglishAnswerProxy)},
        'es': {'slug': 'respuestas',
               'query': SearchQuerySet().models(SpanishAnswerProxy)}
    }
    _map = language_map[language]
    sqs = _map['query']
    query = Clean(request.GET.get('q', ''))
    sqs = sqs.filter(content=query)

    if as_json:
        results = [{'question': result.autocomplete,
                    'url': result.url,
                    'text': result.text}
                   for result in sqs]
        json_results = json.dumps(results)
        return HttpResponse(json_results, content_type='application/json')
    else:
        page = get_object_or_404(
            AnswerResultsPage,
            language=language,
            slug=_map['slug'])
        page.query = query
        page.answers = []

        for result in sqs:
            page.answers.append((result.url, result.autocomplete, result.text))
        return page.serve(request)


def ask_autocomplete(request, language='en'):
    term = request.GET.get(
        'term', '').strip().replace('<', '')
    if not term:
        return JsonResponse([], safe=False)
    if language == 'es':
        sqs = SearchQuerySet().models(SpanishAnswerProxy)
    else:
        sqs = SearchQuerySet().models(EnglishAnswerProxy)
    sqs = sqs.autocomplete(autocomplete=term)
    results = [{'question': result.autocomplete,
                'url': result.url}
               for result in sqs[:20]]
    return JsonResponse(results, safe=False)


def redirect_ask_search(request, language='en'):
    """
    Catch old English pages built via query strings and
    redirect them to category pages if we can. If the query string
    has a 'q' query, we'll run that search.
    """

    cat_string = 'category_exact:'  # the facet prefix for categories
    if request.GET.get('q'):
        querystring = request.GET.get('q')
        if not querystring:
            raise Http404
        return redirect(
            '/ask-cfpb/search/?q={query}'.format(
                query=querystring, permanent=True))
    else:
        facets = request.GET.getlist('selected_facets')
        if not facets:
            raise Http404
        # Get the category, if there is one
        for facet in facets:
            if cat_string in facet:
                category = facet.replace(cat_string, '')
        if not category:
            raise Http404
        if language == 'en':
            return redirect(
                '/ask-cfpb/category-{category}'.format(
                    category=category), permanent=True)
        elif language == 'es':
            return redirect(
                '/es/obtener-respuestas/categoria-{category}'.format(
                    category=category), permanent=True)
