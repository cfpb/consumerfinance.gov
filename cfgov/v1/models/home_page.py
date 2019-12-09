# -*- coding: utf8 -*-
import six

from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, ObjectList, PageChooserPanel, StreamFieldPanel,
    TabbedInterface
)
from wagtail.wagtailadmin.forms import (
    WagtailAdminModelFormMetaclass, WagtailAdminPageForm
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, PageManager
from wagtail.wagtailimages import get_image_model, get_image_model_string
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from flags.state import flag_enabled
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from v1.atomic_elements import molecules
from v1.models.base import CFGOVPage


# These classes are used to add support for nested InlinePanels, and are
# referenced by HomePage.base_form_class. This workaround comes from
# https://github.com/wagtail/wagtail/issues/5511. Proper support for nested
# inline panels in Wagtail won't be added until version 2.8, see
# https://github.com/wagtail/wagtail/pull/5566.
class HomePageFormMetaclass(WagtailAdminModelFormMetaclass):
    @classmethod
    def child_form(cls):
        return HomePageForm


class HomePageForm(
    six.with_metaclass(HomePageFormMetaclass, WagtailAdminPageForm)
):
    pass


class HomePage(CFGOVPage):
    header = StreamField([
        ('info_unit', molecules.InfoUnit()),
        ('half_width_link_blob', molecules.HalfWidthLinkBlob()),
    ], blank=True)

    card_heading = models.CharField(max_length=40, null=True, blank=True)

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
        ObjectList([
            InlinePanel(
                'carousel_items', min_num=4, max_num=4, label="Carousel Item"
            ),
        ], heading='Carousel'),
        ObjectList([
            InlinePanel(
                'info_units', min_num=6, max_num=6, label="Info Unit"
            ),
        ], heading='Info Units'),
        ObjectList([
            FieldPanel('card_heading'),
            InlinePanel('cards', min_num=3, max_num=3, label="Card"),
        ], heading='Cards'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    # Sets page to only be createable at the root
    parent_page_types = ['wagtailcore.Page']

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [index.SearchField('header')]

    base_form_class = HomePageForm

    @property
    def page_js(self):
        return super(HomePage, self).page_js + ['home-page.js']

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['latest_updates'] = self.get_latest_updates(request)

        if flag_enabled('NEW_HOME_PAGE_IN_WAGTAIL', request=request):
            context.update({
                'carousel_items': self.carousel_items.select_related('image'),
                'info_units': [
                    info_unit.as_info_unit()
                    for info_unit in
                    self.info_units.select_related('image')
                ],
                'card_heading': self.card_heading,
                'cards': self.cards.all(),
            })
        elif flag_enabled('NEW_HOME_PAGE', request=request):
            context.update({
                'carousel_items': self.get_hardcoded_carousel_items(),
                'info_units': [
                    molecules.InfoUnit().to_python(info_unit)
                    for info_unit in
                    self.get_hardcoded_info_units()
                ],
                'card_heading': self.get_hardcoded_card_heading(),
                'cards': self.get_hardcoded_cards(),
            })

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

    def get_hardcoded_carousel_items(self):
        images = get_image_model().objects.in_bulk([2514, 2515, 2516, 2517])

        return [
            {
                'title': 'Start Small, Save Up',
                'body': (
                    'Whether you want to put money aside for unexpected '
                    'expenses or make a plan to save for your future goals, we'
                    ' have resources that can help.'
                ),
                'link_text': 'See resources to help you save',
                'link_url': '/start-small-save-up/',
                'image': images[2516],
            },
            {
                'title': 'CFPB Research Conference',
                'body': (
                    u'The CFPB’s fourth research conference features research '
                    u'from a range of disciplines and approaches that inform '
                    'the topic of consumer finance.'
                ),
                'link_text': 'Learn more about the conference',
                'link_url': '/data-research/cfpb-research-conference/',
                'image': images[2515],
            },
            {
                'title': 'Protect yourself from debt collection scams',
                'body': (
                    'Learn how to tell the difference between a legitimate '
                    'debt collector and scammers with our resources.'
                ),
                'link_text': 'Learn how to protect yourself',
                'link_url': (
                    '/about-us/blog/how-tell-difference-between-legitimate-'
                    'debt-collector-and-scammers/'
                ),
                'image': images[2514],
            },
            {
                'title': 'Shop for the best prepaid card for you',
                'body': (
                    u'If you’re considering getting a prepaid card or account,'
                    u' we have information that can help you choose the right '
                    u'one for you and better understand your rights.'
                ),
                'link_text': 'Learn about prepaid cards',
                'link_url': '/consumer-tools/prepaid-cards/',
                'image': images[2517],
            },
        ]

    def get_hardcoded_info_units(self):
        return [
            {
                'image': {
                    'upload': 2503,
                },
                'heading': {
                    'text': 'Empowering consumers',
                    'level': 'h3',
                },
                'body': (
                    'We produce innovative tools and resources to help '
                    'consumers make informed financial decisions, wherever '
                    'they are on their journey.'
                ),
                'links': [
                    {
                        'text': 'Consumer tools',
                        'url': '/consumer-tools/',
                    },
                ],
            },
            {
                'image': {
                    'upload': 2507,
                },
                'heading': {
                    'text': 'Rules of the road',
                    'level': 'h3',
                },
                'body': (
                    'We create clear rules to implement the law and preserve '
                    'choices for consumers.'
                ),
                'links': [
                    {
                        'text': 'Rulemaking',
                        'url': '/policy-compliance/rulemaking/',
                    },
                    {
                        'text': 'Notice and opportunities to comment',
                        'url': (
                            '/policy-compliance/notice-opportunities-comment/'
                        ),
                    },
                ],
            },
            {
                'image': {
                    'upload': 2504,
                },
                'heading': {
                    'text': 'Enforcing the law',
                    'level': 'h3',
                },
                'body': (
                    'We enforce federal consumer financial laws by '
                    'investigating cases of potential wrongdoing and taking '
                    'action.'
                ),
                'links': [
                    {
                        'text': 'Enforcement',
                        'url': '/policy-compliance/enforcement/',
                    },
                    {
                        'text': 'Payments to harmed consumers',
                        'url': '/about-us/payments-harmed-consumers/',
                    }
                ],
            },
            {
                'image': {
                    'upload': 2506,
                },
                'heading': {
                    'text': 'Learning through data and research',
                    'level': 'h3',
                },
                'body': (
                    u'We publish research and information we’ve collected '
                    u'above the consumer financial marketplace.'
                ),
                'links': [
                    {
                        'text': 'Data and research',
                        'url': '/data-research/',
                    },
                    {
                        'text': 'Financial well-being survey data',
                        'url': (
                            '/data-research/financial-well-being-survey-data/'
                        ),
                    },
                ],
            },
            {
                'image': {
                    'upload': 2508,
                },
                'heading': {
                    'text': 'Supervision',
                    'level': 'h3',
                },
                'body': (
                    'We supervise financial companies to ensure compliance '
                    'with federal consumer laws.'
                ),
                'links': [
                    {
                        'text': 'Compliance and guidance',
                        'url': '/policy-compliance/guidance/',
                    },
                    {
                        'text': 'Supervisory highlights',
                        'url': (
                            '/policy-compliance/guidance/'
                            'supervisory-highlights/'
                        ),
                    },
                ],
            },
            {
                'image': {
                    'upload': 2505,
                },
                'heading': {
                    'text': 'Events',
                    'level': 'h3',
                },
                'body': (
                    'We host conferences, workshops, townhalls, symposiums, '
                    'and Advisory Committee meetings.'
                ),
                'links': [
                    {
                        'text': 'Archive of events',
                        'url': '/about-us/events/archive-past-events/',
                    },
                    {
                        'text': 'Request a speaker',
                        'url': '/about-us/events/request-speaker/',
                    },
                ],
            },
        ]

    def get_hardcoded_card_heading(self):
        return "We want to hear from you"

    def get_hardcoded_cards(self):
        return [
            {
                'icon': 'complaint',
                'text': 'Have an issue with a financial product?',
                'link_text': 'Submit a complaint',
                'link_url': '/complaint/',
            },
            {
                'icon': 'lightbulb',
                'text': (
                    'Have a question on a financial topic? '
                    'Browse answers to hundreds of financial questions.'
                ),
                'link_text': 'Browse Ask CFPB',
                'link_url': '/ask-cfpb/',
            },
            {
                'icon': 'open-quote',
                'text': (
                    'Tell us your experiences with money and financial '
                    'services. The CFPB is listening.'
                ),
                'link_text': 'Tell your story',
                'link_url': '/your-story/',
            },
        ]


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


class HomePageCarouselItem(Orderable):
    page = ParentalKey(
        'v1.HomePage', on_delete=models.CASCADE, related_name='carousel_items'
    )
    title = models.CharField(max_length=45, help_text=(
        "45 characters maximum (including spaces). "
        "Sentence case, unless proper noun."
    ))
    body = models.TextField(max_length=160, help_text=(
        "160 characters maximum (including spaces)."
    ))
    link_text = models.CharField(max_length=35, help_text=(
        "35 characters maximum (including spaces). "
        "Lead with a verb, and be specific."
    ))
    # TODO: Change this to use a URLField that also allows relative links.
    # https://code.djangoproject.com/ticket/10896
    link_url = models.CharField("Link URL", max_length=255)
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('link_text'),
        FieldPanel('link_url'),
        ImageChooserPanel('image'),
    ]


class HomePageInfoUnit(ClusterableModel, Orderable):
    page = ParentalKey(
        'v1.HomePage', on_delete=models.CASCADE, related_name='info_units'
    )
    title = models.CharField(max_length=35, help_text=(
        "35 characters maximum (including spaces). "
        "Sentence case, unless proper noun."
    ))
    body = models.TextField(max_length=140, help_text=(
        "140 characters maximum (including spaces)."
    ))
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        ImageChooserPanel('image'),
        # Note: this min_num=1 doesn't seem to work properly, allowing users to
        # save new info units without providing links. This might be due to the
        # incomplete support for nested InlinePanels in our version of Wagtail.
        # See comments above and https://github.com/wagtail/wagtail/pull/5566.
        InlinePanel('links', min_num=1, label="Link"),
    ]

    def as_info_unit(self):
        """Convert model instance into data for molecules.InfoUnit.

        This allows us to use the existing InfoUnit template to render this
        model instance.
        """
        return {
            'image': {
                'upload': self.image,
            },
            'heading': '<h3>%s</h3>' % self.title,
            'body': self.body,
            'links': [
                {
                    'text': link.text,
                    'url': link.url,
                } for link in self.links.all()
            ],
        }


class HomePageInfoUnitLink(Orderable):
    info_unit = ParentalKey(
        'v1.HomePageInfoUnit', on_delete=models.CASCADE, related_name='links'
    )
    text = models.CharField(max_length=40, help_text=(
        "40 characters maximum (including spaces)."
    ))
    # TODO: Change this to use a URLField that also allows relative links.
    # https://code.djangoproject.com/ticket/10896
    url = models.CharField("URL", max_length=255)

    panels = [
        FieldPanel('text'),
        FieldPanel('url'),
    ]


class HomePageCard(Orderable):
    page = ParentalKey(
        'v1.HomePage', on_delete=models.CASCADE, related_name='cards'
    )
    icon = models.CharField(max_length=64, help_text=mark_safe(
        '<a href='
        '"https://cfpb.github.io/design-system/foundation/iconography"'
        '>See full list of icon names.</a>'
    ))
    text = models.TextField(max_length=100, help_text=(
        "100 characters maximum (including spaces)."
    ))
    link_text = models.CharField(max_length=25, help_text=(
        "25 characters maximum (including spaces)."
    ))
    # TODO: Change this to use a URLField that also allows relative links.
    link_url = models.CharField("Link URL", max_length=255)

    panels = [
        FieldPanel('icon'),
        FieldPanel('text'),
        FieldPanel('link_text'),
        FieldPanel('link_url'),
    ]


class SpanishHomePage(HomePage):
    objects = PageManager()
    parent_page_types = ['v1.HomePage']
