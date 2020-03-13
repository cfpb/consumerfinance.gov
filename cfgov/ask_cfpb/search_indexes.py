from django.utils.html import strip_tags
from django.utils.text import Truncator
from haystack import indexes

from search import fields


def truncatissimo(text):
    """Limit preview text to 40 words AND to 255 characters."""
    word_limit = 40
    while word_limit:
        test = Truncator(text).words(word_limit, truncate=' ...')
        if len(test) <= 255:
            return test
        else:
            word_limit -= 1


def extract_raw_text(stream_data):
    # Extract text from stream_data, starting with the answer text.
    text_chunks = [
        block.get('value').get('content')
        for block in stream_data
        if block.get('type') == 'text'
    ]
    extra_chunks = [
        block.get('value').get('content')
        for block in stream_data
        if block.get('type') in ['tip', 'table']
    ]
    chunks = text_chunks + extra_chunks
    return " ".join(chunks)


class AnswerPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = fields.CharFieldWithSynonyms(
        document=True,
        use_template=True,
        boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        use_template=True)
    url = indexes.CharField(
        use_template=True,
        indexed=False)
    tags = indexes.MultiValueField(
        boost=10.0)
    language = indexes.CharField(
        model_attr='language')
    portal_topics = indexes.MultiValueField()
    portal_categories = indexes.MultiValueField()
    suggestions = indexes.FacetCharField()
    preview = indexes.CharField(indexed=False)

    def prepare_preview(self, page):
        raw_text = extract_raw_text(page.answer_content.stream_data)
        full_text = strip_tags(" ".join([page.short_answer, raw_text]))
        return truncatissimo(full_text)

    def prepare_tags(self, page):
        return page.clean_search_tags

    def prepare_portal_topics(self, page):
        return [topic.heading for topic in page.portal_topic.all()]

    def prepare_portal_categories(self, page):
        return [topic.heading for topic in page.portal_category.all()]

    def prepare(self, page):
        self.prepared_data = super(AnswerPageIndex, self).prepare(page)
        self.prepared_data['suggestions'] = self.prepared_data['text']
        return self.prepared_data

    def get_model(self):
        from ask_cfpb.models import AnswerPage
        return AnswerPage

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            live=True, redirect_to_page=None)
