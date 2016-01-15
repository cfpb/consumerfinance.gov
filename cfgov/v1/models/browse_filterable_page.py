import re
import itertools

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from . import base, molecules, organisms, learn_page
from v1.forms import FilterForm


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

    def elements(self):
        return list(itertools.chain(self.header.stream_data,
                    self.content.stream_data))

    def get_context(self, request, *args, **kwargs):
        context = super(BrowseFilterablePage, self).get_context(request, *args,
                                                                **kwargs)
        context['forms'] = []
        form_specific_filters = self.get_form_specific_filters(request.GET)
        form_types = [f['value']['form_type']
                      for f in self.content.stream_data
                      if 'filter_controls' in f['type']]
        forms = [FilterForm(form_specific_filters[filters_id])
                 for type, filters_id in zip(form_types, form_specific_filters)
                 if 'filterable-list' in type]
        for form in forms:
            if form.is_valid():
                # List of pages to pass to the template
                page_set = \
                    learn_page.AbstractLearnPage.objects.live().filter(
                        form.generate_query())
                paginator = Paginator(page_set.order_by('-date_published'),
                                      10)
                page = request.GET.get('page')

                try:
                    posts = paginator.page(page)
                except PageNotAnInteger:
                    posts = paginator.page(1)
                except EmptyPage:
                    posts = paginator.page(paginator.num_pages)

                context.update({'posts': posts})
            else:
                print form.errors
            context['forms'].append(form)
        return context

    def get_form_specific_filters(self, request_dict):
        forms = {}
        for name in request_dict:
            if re.search(r'\d+', name):
                form_id = int(re.search(r'\d+', name).group())
                forms[form_id] = {}
        for f_id in forms.keys():
            for field in FilterForm.declared_fields:
                request_field_name = 'filter' + str(f_id) + '_' + field
                if 'categories' in field:
                    if forms[f_id].get(field):
                        forms[f_id][field].append(
                            request_dict.get(request_field_name))
                    else:
                        forms[f_id].update({
                            field: [request_dict.get(request_field_name)]
                        })
        return forms
