from __future__ import unicode_literals
import json

# from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from haystack.inputs import Clean

from django.shortcuts import get_object_or_404, redirect  # render_to_response
from django.http import HttpResponse

from .models import (
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
    if language == 'en':
        sqs = SearchQuerySet().models(EnglishAnswerProxy)
    elif language == 'es':
        sqs = SearchQuerySet().models(SpanishAnswerProxy)
    sqs = sqs.filter(content=Clean(request.GET.get('q', '')))

    if as_json:
        results = [{'question': result.autocomplete,
                    'url': result.url}
                   for result in sqs]
        json_results = json.dumps(results)
        return HttpResponse(json_results, content_type='application/json')
    else:
        page = get_object_or_404(
            AnswerResultsPage,
            language=language)
        page.answers = []
        for result in sqs:
            page.answers.append((result.url, result.autocomplete))
        return page.serve(request)


def ask_autocomplete(request, language='en'):
    term = request.GET.get('term', '').strip()
    if language == 'en':
        sqs = SearchQuerySet().models(EnglishAnswerProxy)
        sqs = sqs.filter()
        sqs = sqs.autocomplete(autocomplete=term)
    elif language == 'es':
        sqs = SearchQuerySet().models(SpanishAnswerProxy)
        sqs = sqs.filter()
        sqs = sqs.autocomplete(autocomplete=term)
    return HttpResponse(json.dumps(sqs), content_type="application/json")
