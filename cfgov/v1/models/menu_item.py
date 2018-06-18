from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
)
from wagtail.wagtailcore.fields import StreamField

from v1 import blocks as v1_blocks


@python_2_unicode_compatible
class MenuItem(models.Model):
    link_text = models.CharField(
        max_length=255,
        help_text='Display text for menu link',
        verbose_name="Menu label")

    external_link = models.CharField(
        null=True,
        blank=True,
        max_length=1000,
        help_text='Enter url for page outside Wagtail. This will only '
                  'be used if there is no page selected.',
        default='#',
        verbose_name='Direct URL (rare)')

    page_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        help_text='Link to a page in Wagtail.',
        verbose_name='Overview page link'
    )

    order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Determines order in which this menu item appears in nav.'
    )

    column_1 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label='Menu items group'),)
    ], blank=True)

    column_2 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label='Menu items group'))
    ], blank=True)

    column_3 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label='Menu items group'))
    ], blank=True)

    column_4 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label='Menu items group')),
        ('featured_content', v1_blocks.FeaturedMenuContent(
            label='Featured image item'))
    ], blank=True)

    nav_footer = StreamField([
        ('nav_footer', v1_blocks.NavFooter(
            label='Menu footer'))
    ], blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('link_text'),
            PageChooserPanel('page_link'),
            FieldPanel('external_link'),
        ], heading='Menu Information'),
        FieldPanel('order'),
        StreamFieldPanel('column_1'),
        StreamFieldPanel('column_2'),
        StreamFieldPanel('column_3'),
        StreamFieldPanel('column_4'),
        StreamFieldPanel('nav_footer'),
    ]

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.link_text

    def get_content(self, draft):
        """
        Filter menu item column content by by draft/live state
        and structure it for display in menu template.
        """
        cols = [getattr(self, 'column_' + str(i)) for i in range(1, 5)]
        self.nav_groups = filter(None, [self.get_active_block(col, draft)
                                        for col in cols])
        self.featured_content = self.nav_groups.pop() if len(self.nav_groups) \
            and self.nav_groups[-1].block_type == 'featured_content' else None
        self.footer = self.get_active_block(self.nav_footer, draft)
        return self

    @staticmethod
    def get_active_block(blocks, draft):
        """
        Returns first block whose state matches draft
        parameter. If draft parameter is true, will
        return last live block if there are no draft blocks.
        """
        return next((block for i, block in enumerate(blocks) if
                    block.value.get('draft', '') == draft or
                    (draft and i == len(blocks) - 1)), None)
