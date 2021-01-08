from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel,
    TabbedInterface
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, PageManager
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from modelcluster.fields import ParentalKey

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage
from v1.models.learn_page import AbstractFilterPage
from v1.util.ref import (
    enforcement_at_risk_groups, enforcement_defendant_types,
    enforcement_products, enforcement_statuses, enforcement_statutes
)


def make_dec():
    return models.DecimalField(
        decimal_places=2,
        max_digits=13,
        default=0
    )


class EnforcementActionDisposition(models.Model):
    final_disposition = models.CharField(max_length=150, blank=True)
    final_disposition_type = models.CharField(
        max_length=15,
        choices=[('Final Order', 'Final Order'), ('Dismissal', 'Dismissal')],
        blank=True
    )
    final_order_date = models.DateField(null=True, blank=True)
    dismissal_date = models.DateField(null=True, blank=True)
    final_order_consumer_redress = make_dec()
    final_order_consumer_redress_suspended = make_dec()
    final_order_other_consumer_relief = make_dec()
    final_order_other_consumer_relief_suspended = make_dec()
    final_order_disgorgement = make_dec()
    final_order_disgorgement_suspended = make_dec()
    final_order_civil_money_penalty = make_dec()
    final_order_civil_money_penalty_suspended = make_dec()
    estimated_consumers_entitled_to_relief = models.CharField(
        max_length=30,
        default=0
    )

    action = ParentalKey(
        'v1.EnforcementActionPage',
        on_delete=models.CASCADE,
        related_name='enforcement_dispositions'
    )


# Will exist until can be sourced from enforce db
class EnforcementActionStatus(models.Model):
    status = models.CharField(max_length=50, choices=enforcement_statuses)
    action = ParentalKey('v1.EnforcementActionPage',
                         on_delete=models.CASCADE,
                         related_name='statuses')


# Will exist until can be sourced from enforce db
class EnforcementActionDocket(models.Model):
    docket_number = models.CharField(max_length=50)
    action = ParentalKey('v1.EnforcementActionPage',
                         on_delete=models.CASCADE,
                         related_name='docket_numbers')


class EnforcementActionDefendantType(models.Model):
    defendant_type = models.CharField(
        max_length=15, choices=enforcement_defendant_types, blank=True
    )
    action = ParentalKey('v1.EnforcementActionPage',
                         on_delete=models.CASCADE,
                         related_name='defendant_types')


class EnforcementActionProduct(models.Model):
    product = models.CharField(
        max_length=50, choices=enforcement_products
    )
    action = ParentalKey('v1.EnforcementActionPage',
                         on_delete=models.CASCADE,
                         related_name='products')


class EnforcementActionAtRisk(models.Model):
    at_risk_group = models.CharField(
        max_length=30, choices=enforcement_at_risk_groups
    )
    action = ParentalKey('v1.EnforcementActionPage',
                         on_delete=models.CASCADE,
                         related_name='at_risk_groups')


class EnforcementActionStatute(models.Model):
    statute = models.CharField(
        max_length=30, choices=enforcement_statutes
    )
    action = ParentalKey('v1.EnforcementActionPage',
                         on_delete=models.CASCADE,
                         related_name='statutes')


class EnforcementActionPage(AbstractFilterPage):
    public_enforcement_action = models.CharField(max_length=150, blank=True)
    initial_filing_date = models.DateField(null=True, blank=True)
    settled_or_contested_at_filing = models.CharField(
        max_length=10,
        choices=[('Settled', 'Settled'), ('Contested', 'Contested')],
        blank=True
    )
    court = models.CharField(default='', max_length=150, blank=True)

    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', organisms.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('notification', molecules.Notification()),
        ('table_block', organisms.AtomicTableBlock(
            table_options={'renderer': 'html'})),
        ('feedback', v1_blocks.Feedback()),
    ], blank=True)

    content_panels = [
        StreamFieldPanel('header'),
        StreamFieldPanel('content')
    ]

    metadata_panels = [
        FieldPanel('public_enforcement_action'),
        FieldPanel('initial_filing_date'),
        InlinePanel('defendant_types', label='Defendant/Respondent Type'),
        InlinePanel('categories', label="Forum", min_num=1, max_num=2),
        FieldPanel('court'),
        InlinePanel('docket_numbers', label="Docket Number", min_num=1),
        FieldPanel('settled_or_contested_at_filing'),
        InlinePanel('statuses', label="Status", min_num=1),
        InlinePanel('products', label="Products"),
        InlinePanel('at_risk_groups', label="At Risk Groups"),
        InlinePanel('statutes', label="Statutes/Regulations"),
        InlinePanel(
            'enforcement_dispositions',
            label='Final Disposition'
        ),
    ]

    settings_panels = [
        MultiFieldPanel(CFGOVPage.promote_panels, 'Settings'),
        MultiFieldPanel([
            FieldPanel('preview_title'),
            FieldPanel('preview_subheading'),
            FieldPanel('preview_description'),
            FieldPanel('secondary_link_url'),
            FieldPanel('secondary_link_text'),
            ImageChooserPanel('preview_image'),
        ], heading='Page Preview Fields', classname='collapsible'),
        FieldPanel('authors', 'Authors'),
        MultiFieldPanel([
            FieldPanel('date_published'),
            FieldPanel('comments_close_by'),
        ], 'Relevant Dates', classname='collapsible'),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
        FieldPanel('language', 'Language'),
        MultiFieldPanel(CFGOVPage.archive_panels, 'Archive'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(
            AbstractFilterPage.content_panels + content_panels,
            heading='General Content'
        ),
        ObjectList(metadata_panels, heading='Metadata'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(settings_panels, heading='Configuration')
    ])

    template = 'enforcement-action/index.html'

    objects = PageManager()

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]

    def get_context(self, request):
        context = super(EnforcementActionPage, self).get_context(request)
        dispositions = self.enforcement_dispositions.all()

        context.update({
            'total_consumer_relief': sum(
                disp.final_order_consumer_redress +
                disp.final_order_other_consumer_relief
                for disp in dispositions
            ),
            'total_cmp': sum(
                disp.final_order_civil_money_penalty
                for disp in dispositions
            ),
            'statutes': [s.statute for s in self.statutes.all()],
            'products': [p.product for p in self.products.all()],
            'at_risk_groups': [
                g.at_risk_group for g in self.at_risk_groups.all()
            ]
        })

        return context
