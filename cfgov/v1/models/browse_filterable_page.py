from operator import attrgetter

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from . import base, molecules, organisms, ref
from .learn_page import AbstractFilterPage
from .. import forms


class BrowseFilterablePage(base.CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
    ])
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterControls()),
    ])

    # General content tab
    content_panels = base.CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(base.CFGOVPage.sidefoot_panels, heading='Footer'),
        ObjectList(base.CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'browse-filterable/index.html'

    def get_context(self, request, *args, **kwargs):
        context = super(BrowseFilterablePage, self).get_context(request, *args,
                                                                **kwargs)
        context['forms'] = []
        form_class = self.get_form_class()
        form_specific_filters = self.get_form_specific_filter_data(form_class,
                                                                   request.GET)
        forms = [form_class(form_specific_filters[filters_id], parent=self)
                 for filters_id in form_specific_filters.keys()]
        for form in forms:
            if form.is_valid():
                # Paginate results by 10 items per page.
                paginator = Paginator(self.get_page_set(form, request.site.hostname), 10)
                page = request.GET.get('page')

                # Get the page number in the request and get the page from the
                # paginator to serve.
                try:
                    posts = paginator.page(page)
                except PageNotAnInteger:
                    posts = paginator.page(1)
                except EmptyPage:
                    posts = paginator.page(paginator.num_pages)

                context.update({'posts': posts})
            context['forms'].append(form)
        return context

    def get_form_class(self):
        return forms.FilterableListForm

    # Transform each GET parameter key from unique ID for the form in the
    # request and assign it to a dictionary under the form ID from where it
    # came from.
    def get_form_specific_filter_data(self, form_class, request_dict):
        filters_data = {}
        # Find every form existing on the page and assign a dictionary with its
        # number as the key.
        for i, f in enumerate(self.content):
            if 'filter_controls' in f.block_type:
                filters_data[i] = {}

        # For each form ID dictionary, find all the fields for it. Assign the
        # select fields to lists and append them for each selection. Return the
        # dictionary of normalized field names with their respective data.
        for i in filters_data.keys():
            for field in form_class.declared_fields:
                request_field_name = 'filter' + str(i) + '_' + field
                if field in ['categories', 'topics', 'authors']:
                    filters_data[i][field] = \
                        request_dict.getlist(request_field_name, [])
                else:
                    filters_data[i][field] = \
                        request_dict.get(request_field_name, '')
        return filters_data

    # Returns a queryset of AbstractFilterPages
    def get_page_set(self, form, hostname):
        # If this is the Newsroom, then we need to go get the blog
        # from a different part of the site.
        blog_q = Q()
        for f in self.content:
            if 'filter_controls' in f.block_type and 'newsroom' in \
                    f.value['categories']['page_type']:
                categories = form.cleaned_data.get('categories', [])
                if not categories or 'blog' in categories:
                    blog_cats = [c[0] for c in ref.categories[1][1]]
                    blog_q = Q('categories__name__in', blog_cats)
        # If this is the staging site, then return pages that are
        # shared. Else, make sure that the pages are published.
        if getattr(settings, 'STAGING_HOSTNAME', 'content') in hostname:
            return AbstractFilterPage.objects.filter(
                shared=True).descendant_of(self).filter(form.generate_query() | blog_q)
        else:
            return AbstractFilterPage.objects.live().descendant_of(
                self).filter(form.generate_query() | blog_q)


class EventArchivePage(BrowseFilterablePage):
    def get_form_class(self):
        return forms.EventArchiveFilterForm

    def get_template(self, request, *args, **kwargs):
        return BrowseFilterablePage.template
