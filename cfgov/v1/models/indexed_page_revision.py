from wagtail.models import PageRevision
from wagtail.search import index


class IndexedPageRevision(index.Indexed, PageRevision):
    search_fields = [
        index.SearchField("content"),
        index.FilterField("created_at"),
    ]

    class Meta:
        proxy = True
