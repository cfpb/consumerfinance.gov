# -*- coding: utf8 -*-
from django.db import models
from django.db.models import Q

from wagtail.wagtailadmin.edit_handlers import (
    InlinePanel, ObjectList, PageChooserPanel, StreamFieldPanel,
    TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailimages import get_image_model
from wagtail.wagtailsearch import index

from flags.state import flag_enabled
from modelcluster.fields import ParentalKey

from v1.atomic_elements import molecules
from v1.models.base import CFGOVPage
from v1.util import ref


"""Placeholder until these are exposed in the Wagtail admin."""
_carousel_items_by_language = {
    'en': [
        {
            'title': 'Start Small, Save Up',
            'body': (
                'Whether you want to put money aside for unexpected expenses '
                'or make a plan to save for your future goals, we have '
                'resources that can help.'
            ),
            'link': {
                'text': 'Learn how to get started',
                'url': '/start-small-save-up/',
            },
            'image_pk': 2516,
        },
        {
            'title': 'CFPB Research Conference',
            'body': (
                'CFPB hosting research conference featuring research from a '
                'range of disciplines and approaches that can inform the '
                'topic of consumer finance.'
            ),
            'link': {
                'text': 'Learn about the conference',
                'url': '/data-research/cfpb-research-conference/',
            },
            'image_pk': 2515,
        },
        {
            'title': 'Protect yourself from debt collection scams',
            'body': (
                'Watch our new video to learn how to tell the difference '
                'between legitimate debt collector and scammers'
            ),
            'link': {
                'text': 'Learn how to protect yourself',
                'url': (
                    '/about-us/blog/how-tell-difference-between-legitimate-'
                    'debt-collector-and-scammers/'
                ),
            },
            'image_pk': 2514,
        },
        {
            'title': 'TODO',
            'body': (
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In '
                'pellentesque odio et nulla ornare porta. Nulla lobortis '
                'tincidunt congue nullam.'
            ),
            'link': {
                'text': 'TODO',
                'url': '/',
            },
            'image_pk': 2516,
        },
    ],
}


# TODO: Add real carousel content for Spanish.
_carousel_items_by_language['es'] = _carousel_items_by_language['en']


"""Placeholder until these are exposed in the Wagtail admin."""
_info_units_by_language = {
    'en': [
        {
            'image': {
                'upload': 2503,
            },
            'heading': {
                'text': 'Empowering consumers',
                'level': 'h3',
            },
            'body': (
                'We produce innovative tools and resources to help consumers '
                'make informed financial decisions, wherever they are on '
                'their journey.'
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
                    'url': '/policy-compliance/notice-opportunities-comment/'
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
                'We enforce federal consumer financial laws by investigating '
                'cases of potential wrongdoing and taking action.'
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
                u'We publish research and information we’ve collected above '
                u'the consumer financial marketplace.'
            ),
            'links': [
                {
                    'text': 'Data and research',
                    'url': '/data-research/',
                },
                {
                    'text': 'Financial well-being survey data',
                    'url': '/data-research/financial-well-being-survey-data/',
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
                'We supervise financial companies to ensure compliance with '
                'federal consumer laws.'
            ),
            'links': [
                {
                    'text': 'Compliance and guidance',
                    'url': '/policy-compliance/guidance/',
                },
                {
                    'text': 'Supervisory highlights',
                    'url': (
                        '/policy-compliance/guidance/supervisory-highlights/'
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
                'We host conferences, workshops, townhalls, symposiums, and '
                'Advisory Committee meetings.'
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
    ],
}


# TODO: Add real info unit content for Spanish.
_info_units_by_language['es'] = _info_units_by_language['en']


_cards_by_language = {
    'en': [
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
                'Tell us your experiences with money and financial services. '
                'The CFPB is listening.'
            ),
            'link_text': 'Tell your story',
            'link_url': '/your-story/',
        },
    ],
}


# TODO: Add real card content for Spanish.
_cards_by_language['es'] = _cards_by_language['en']


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
        context.update({
            'carousel_items': self.get_carousel_items(),
            'get_image_instance': self.get_image_instance,
            'info_units': self.get_info_units(),
            # TODO: Add Spanish version of this heading.
            'card_heading': "We want to hear from you",
            'cards': self.get_cards(),
            'latest_updates': self.get_latest_updates(request),
        })
        return context

    def get_carousel_items(self):
        return _carousel_items_by_language[self.language]

    def get_image_instance(self, pk):
        # TODO: Not needed once the entire carousel is in Wagtail.
        return get_image_model().objects.get(pk=pk)

    def get_info_units(self):
        return [
            molecules.InfoUnit().to_python(info_unit)
            for info_unit in _info_units_by_language[self.language]
        ]

    def get_cards(self):
        return _cards_by_language[self.language]

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
