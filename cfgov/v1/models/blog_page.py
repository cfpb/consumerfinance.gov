from datetime import date

from django.core.validators import RegexValidator
from django.db import models
from localflavor.us.models import USStateField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, FieldRowPanel,
                                                InlinePanel, MultiFieldPanel,
                                                ObjectList, StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from . import AbstractFilterPage, CFGOVPageManager
from .. import blocks as v1_blocks
from ..atomic_elements import molecules, organisms


class BlogPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('feedback', v1_blocks.Feedback()),
    ])
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel = StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'

    objects = PageManager()


class LegacyBlogPage(AbstractFilterPage):
    content = StreamField([
        ('content', blocks.RawHTMLBlock(help_text='Content from WordPress unescaped.')),
        ('feedback', v1_blocks.Feedback()),
    ])
    objects = CFGOVPageManager()
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel = StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'
