from __future__ import unicode_literals
import json

from haystack.query import SearchQuerySet
from haystack.inputs import Clean

from django.shortcuts import get_object_or_404, redirect  # render_to_response
from django.http import HttpResponse, JsonResponse

from ask_cfpb.models import (
    AnswerPage,
    AnswerResultsPage,
    EnglishAnswerProxy,
    SpanishAnswerProxy)


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
    slug_map = {
        'en': 'ask-cfpb-search-results',
        'es': 'respuestas'
    }
    if language == 'en':
        sqs = SearchQuerySet().models(EnglishAnswerProxy)
    elif language == 'es':
        sqs = SearchQuerySet().models(SpanishAnswerProxy)
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
            slug=slug_map[language])
        page.query = query
        page.answers = []

        for result in sqs:
            page.answers.append((result.url, result.autocomplete, result.text))
        return page.serve(request)


def ask_autocomplete(request, language='en'):
    term = request.GET.get(
        'term', '').strip().replace('<', '')
    if language == 'es':
        sqs = SearchQuerySet().models(SpanishAnswerProxy)
    else:
        sqs = SearchQuerySet().models(EnglishAnswerProxy)
    sqs = sqs.autocomplete(autocomplete=term)
    results = [{'question': result.autocomplete,
                'url': result.url}
               for result in sqs[:20]]
    return JsonResponse(results, safe=False)
