from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from ask_cfpb.models import blocks as ask_blocks
from v1 import blocks as v1_blocks
from v1.atomic_elements import organisms
from v1.feeds import get_appropriate_rss_feed_url_for_page
from v1.models.base import CFGOVPageManager
from v1.models.learn_page import AbstractFilterPage


class BlogPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('video_player', organisms.VideoPlayer()),
        ('email_signup', organisms.EmailSignUp()),
        ('feedback', v1_blocks.Feedback()),
        ('faq_schema', ask_blocks.FAQ(label='FAQ schema')),
        ('how_to_schema', ask_blocks.HowTo(label='HowTo schema'))
    ])
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'

    objects = PageManager()
    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)

        context['rss_feed'] = get_appropriate_rss_feed_url_for_page(
            self,
            request=request
        )

        return context


class LegacyBlogPage(AbstractFilterPage):
    content = StreamField([
        ('content', blocks.RawHTMLBlock(
            help_text='Content from WordPress unescaped.'
        )),
        ('feedback', v1_blocks.Feedback()),
        ('reusable_text', v1_blocks.ReusableTextChooserBlock(
            'v1.ReusableText'
        )),
    ])
    objects = CFGOVPageManager()
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]
