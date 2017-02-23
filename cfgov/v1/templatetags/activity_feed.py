from v1.models.learn_page import AbstractFilterPage
from v1.util.categories import clean_categories


def get_latest_activities(activity_type, hostname, quantity=5):
    categories = clean_categories([activity_type])
    return AbstractFilterPage.objects.live_shared(hostname).filter(
        categories__name__in=categories
    ).order_by('-date_published')[:quantity]
