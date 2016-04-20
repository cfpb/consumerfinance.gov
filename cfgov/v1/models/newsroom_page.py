from datetime import date
from localflavor.us.models import USStateField

from django.db import models
from django.core.validators import RegexValidator
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from . import molecules
from . import organisms
from . import BlogPage, LegacyBlogPage, CFGOVPageManager


class NewsroomPage(BlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()


class LegacyNewsroomPage(LegacyBlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()
