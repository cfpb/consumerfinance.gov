from wagtail.core.models import PageRevision
from wagtail.search import index


class IndexedPageRevision(index.Indexed, PageRevision):

    search_fields = [
        index.SearchField("content_json"),
        index.FilterField("created_at"),
    ]

    class Meta:
        proxy = True
