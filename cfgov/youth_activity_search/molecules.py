from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class YouthSearchHeroImage(blocks.StructBlock):
    image = ImageChooserBlock(
        help_text='Should be exactly 390px tall, and up to 940px wide, '
                  'unless this is an overlay or bleeding style hero.'
    )
    small_image = ImageChooserBlock(
        required=False,
        help_text='Provide an alternate image for small displays '
                  'when using a bleeding or overlay hero.'
    )

    class Meta:
        icon = 'image'
        template = 'youth_activity_search/activity_search_hero_image.html'
        label = 'Image'
