from django.core.management.base import BaseCommand

from wagtail.wagtailimages import get_image_model

from v1.models.home_page import (
    HomePage, HomePageCard, HomePageCarouselItem, HomePageInfoUnit,
    HomePageInfoUnitLink
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        pages = HomePage.objects.in_bulk([
            319,    # English home page, at /
            12786,  # Spanish home page, at /es/
        ])

        for page in pages.values():
            self.update(page)

    def update(self, page):
        page.carousel_items = [
            HomePageCarouselItem(**item)
            for item in page.get_hardcoded_carousel_items()
        ]

        page.info_units = [
            HomePageInfoUnit(
                title=iu['heading']['text'],
                body=iu['body'],
                image=get_image_model().objects.get(pk=iu['image']['upload']),
                links=[
                    HomePageInfoUnitLink(**link)
                    for link in iu['links']
                ]
            ) for iu in page.get_hardcoded_info_units()
        ]

        page.card_heading = page.get_hardcoded_card_heading()

        page.cards = [
            HomePageCard(**card)
            for card in page.get_hardcoded_cards()
        ]

        page.save_revision()
