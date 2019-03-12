from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailsearch import index

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
        ('email_signup', organisms.EmailSignUp()),
        ('feedback', v1_blocks.Feedback()),
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
    ])
    objects = CFGOVPageManager()
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]
