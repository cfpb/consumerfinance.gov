from __future__ import unicode_literals

from wagtail.wagtailadmin.edit_handlers import (
    ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField

from paying_for_college.blocks import GuidedQuiz

from v1.atomic_elements import molecules, organisms
from v1.models import CFGOVPage, CFGOVPageManager


class RepayingStudentDebtPage(CFGOVPage):
    """A page to serve static subpages in the paying-for-college suite."""
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', organisms.FeaturedContent()),
    ], blank=True)

    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('raw_html_block', blocks.RawHTMLBlock(
            label='Raw HTML block'
        )),
    ], blank=True)

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])
    objects = CFGOVPageManager()

    def get_template(self, request):
        return 'paying-for-college/repaying-student-debt.html'

    @property
    def page_js(self):
        return (super(
            RepayingStudentDebtPage, self).page_js +
            ['secondary-navigation.js']
        )


class StudentLoanQuizPage(CFGOVPage):
    """A page to guide students through the college debt maze."""
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', organisms.FeaturedContent()),
    ], blank=True)

    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('guided_quiz', GuidedQuiz()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('raw_html_block', blocks.RawHTMLBlock(
            label='Raw HTML block'
        )),
    ], blank=True)

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])
    objects = CFGOVPageManager()

    def get_template(self, request):
        for block in self.content:
            block.value['situation_id'] = block.id
        return 'paying-for-college/choose-a-student-loan.html'.format(
            self.slug)

    @property
    def page_js(self):
        return (super(
            StudentLoanQuizPage, self).page_js + ['secondary-navigation.js']
        )


class CollegeCostsPage(CFGOVPage):
    """Breaking down financial aid and loans for prospectives student."""
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', organisms.FeaturedContent()),
    ], blank=True)

    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('raw_html_block', blocks.RawHTMLBlock(
            label='Raw HTML block'
        )),
    ], blank=True)

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])
    objects = CFGOVPageManager()

    def get_template(self, request):
        return 'paying-for-college/college-costs.html'

    @property
    def page_js(self):
        return (super(
            CollegeCostsPage, self).page_js + ['secondary-navigation.js']
        )
