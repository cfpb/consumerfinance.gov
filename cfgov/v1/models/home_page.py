from django.db import models
from django.db.models import Q

from wagtail.wagtailadmin.edit_handlers import (
    InlinePanel, ObjectList, PageChooserPanel, StreamFieldPanel,
    TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailsearch import index

from flags.state import flag_enabled
from modelcluster.fields import ParentalKey

from v1.atomic_elements import molecules
from v1.models.base import CFGOVPage
from v1.util import ref


class HomePage(CFGOVPage):
    header = StreamField([
        ('info_unit', molecules.InfoUnit()),
        ('half_width_link_blob', molecules.HalfWidthLinkBlob()),
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        InlinePanel(
            'excluded_updates',
            label='Pages excluded from Latest Updates',
            help_text=('This block automatically displays the six most '
                       'recently published blog posts, press releases, '
                       'speeches, testimonies, events, or op-eds. If you want '
                       'to exclude a page from appearing as a recent update '
                       'in this block, add it as an excluded page.')
        ),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    # Sets page to only be createable at the root
    parent_page_types = ['wagtailcore.Page']

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [index.SearchField('header')]

    @property
    def page_js(self):
        return super(HomePage, self).page_js + ['home-page.js']

    def get_category_name(self, category_icon_name):
        cats = dict(ref.limited_categories)
        return cats[str(category_icon_name)]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['latest_updates'] = self.get_latest_updates(request)
        return context

    def get_latest_updates(self, request):
        # TODO: There should be a way to express this as part of the query
        # rather than evaluating it in Python.
        excluded_updates_pks = [
            e.excluded_page.pk for e in self.excluded_updates.all()
        ]

        latest_pages = CFGOVPage.objects.in_site(
            request.site
        ).exclude(
            pk__in=excluded_updates_pks
        ).filter(
            Q(content_type__app_label='v1') & (
                Q(content_type__model='blogpage') |
                Q(content_type__model='eventpage') |
                Q(content_type__model='newsroompage')
            ),
            live=True,
        ).distinct().order_by(
            '-first_published_at'
        )[:6]

        return latest_pages

    def get_template(self, request):
        if flag_enabled('NEW_HOME_PAGE', request=request):
            return 'home-page/index_new.html'
        else:
            return 'home-page/index_%s.html' % self.language


class HomePageExcludedUpdates(models.Model):
    page = ParentalKey(
        HomePage, on_delete=models.CASCADE, related_name='excluded_updates'
    )
    excluded_page = models.ForeignKey(
        CFGOVPage, on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        PageChooserPanel('excluded_page'),
    ]


class SpanishHomePage(HomePage):
    objects = PageManager()
    parent_page_types = ['v1.HomePage']
