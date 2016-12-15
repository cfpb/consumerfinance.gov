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
from wagtail.wagtailcore.models import Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from . import BlogPage, CFGOVPageManager, LegacyBlogPage
from ..atomic_elements import molecules, organisms


class NewsroomPage(BlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()


class LegacyNewsroomPage(LegacyBlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()
