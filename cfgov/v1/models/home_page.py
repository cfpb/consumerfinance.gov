# -*- coding: utf8 -*-
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

from v1.atomic_elements import atoms, molecules
from v1.models.base import CFGOVPage
from v1.util import ref


"""Placeholder until these are exposed in the Wagtail admin."""
_placeholder_carousel_image = {
    'alt': 'Alt text goes here',
    'upload': 2509,
}


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
            'image': _placeholder_carousel_image,
        },
        {
            'title': 'Tax time',
            'body': (
                'Take advantage of the time when you are filing your tax '
                'return to set aside a portion of your refund towards savings.'
            ),
            'link': {
                'text': 'Learn more about tax time savings',
                'url': '/about-us/blog/tax-time-saving-tips/',
            },
            'image': _placeholder_carousel_image,
        },
        {
            'title': 'Building a Bridge to Credit Visibility Symposium',
            'body': (
                'Mark your Calendar to join the Bureau for a day-long '
                'symposium on September 17, 2018, from 8:00am to 4:45pm'
            ),
            'link': {
                'text': 'Learn more about this event',
                'url': (
                    '/about-us/events/archive-past-events'
                    '/building-bridge-credit-visibility/'
                ),
            },
            'image': _placeholder_carousel_image,
        },
        {
            'title': 'Equifax data breach updates',
            'body': (
                'Today the CFPB, FTC and States Announced Settlement with '
                'Equifax Over 2017 Data Breach.'
            ),
            'link': {
                'text': 'Find out more details',
                'url': '/equifax-settlement/',
            },
            'image': _placeholder_carousel_image,
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
                'alt': 'Alt text goes here',
                'upload': 2503,
            },
            'heading': {
                'text': 'Empowering Consumers',
                'level': 'h3',
            },
            'body': (
                'We produce innovation products to help consumers make '
                'informed financial decisions and choose products and '
                'services that fit their needs.'
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
                'alt': 'Alt text goes here',
                'upload': 2507,
            },
            'heading': {
                'text': 'Rules of the Road',
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
                    'text': 'Notice and Opportunities to Comment',
                    'url': '/policy-compliance/notice-opportunities-comment/'
                },
            ],
        },
        {
            'image': {
                'alt': 'Alt text goes here',
                'upload': 2504,
            },
            'heading': {
                'text': 'Enforcing the Law',
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
                'alt': 'Alt text goes here',
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
                    'text': 'Data and Research',
                    'url': '/data-research/',
                },
                {
                    'text': 'Financial Well-being survey',
                    'url': '/data-research/financial-well-being-survey-data/',
                },
            ],
        },
        {
            'image': {
                'alt': 'Alt text goes here',
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
                    'text': 'Compliance and Guidance',
                    'url': '/policy-compliance/guidance/',
                },
                {
                    'text': 'Supervisory Highlights',
                    'url': (
                        '/policy-compliance/guidance/supervisory-highlights/'
                    ),
                },
            ],
        },
        {
            'image': {
                'alt': 'Alt text goes here',
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
                    'text': 'Archive of Events',
                    'url': '/about-us/events/archive-past-events/',
                },
                {
                    'text': 'Request a Speaker',
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
            'make_image_atom': self.make_image_atom,
            'info_units': self.get_info_units(),
            # TODO: Add Spanish version of this heading.
            'card_heading': "We want to hear from you",
            'cards': self.get_cards(),
            'latest_updates': self.get_latest_updates(request),
        })
        return context

    def get_carousel_items(self):
        return _carousel_items_by_language[self.language]

    def make_image_atom(self, value):
        # TODO: Not needed once the entire carousel is in Wagtail.
        return atoms.ImageBasic().to_python(value)

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
