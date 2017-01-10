from datetime import date
from localflavor.us.models import USStateField

from django.db import models
from django.core.validators import RegexValidator
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from . import AbstractFilterPage
from ..atomic_elements import molecules, organisms
from .. import blocks as v1_blocks

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


class LegacyBlogPage(AbstractFilterPage):
    content = StreamField([
        ('content', blocks.RawHTMLBlock(help_text='Content from WordPress unescaped.')),
        ('feedback', v1_blocks.Feedback()),
    ])
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel = StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'
