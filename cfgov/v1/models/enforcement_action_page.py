from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
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


enforcement_statuses = [
    ("expired-terminated-dismissed", "Expired/Terminated/Dismissed"),
    ("pending-litigation", "Pending Litigation"),
    ("post-order-post-judgment", "Post Order/Post Judgment"),
]

enforcement_defendant_types = [
    ("Non-Bank", "Nonbank"),
    ("Bank", "Bank"),
    ("Individual", "Individual"),
]

enforcement_products = [
    ("Auto Finance Origination", "Auto Finance Origination"),
    ("Auto Finance Servicing", "Auto Finance Servicing"),
    ("Business Lending (ECOA)", "Business Lending (ECOA)"),
    ("Consumer Reporting Agencies", "Consumer Reporting Agencies"),
    ("Consumer Reporting ? User", "Consumer Reporting - User"),
    ("Credit Cards", "Credit Cards"),
    ("Credit Repair", "Credit Repair"),
    ("Debt Collection", "Debt Collection"),
    ("Debt Relief", "Debt Relief"),
    ("Deposits", "Deposits"),
    ("Furnishing", "Furnishing"),
    ("Fair Lending", "Fair Lending"),
    ("Mortgage Origination", "Mortgage Origination"),
    ("Mortgage Servicing", "Mortgage Servicing"),
    ("Payments", "Payments"),
    ("Prepaid", "Prepaid"),
    ("Remittances", "Remittances"),
    ("Short Term, Small Dollar", "Short Term, Small Dollar"),
    ("Student Loan Origination", "Student Loan Origination"),
    ("Student Loan Servicing", "Student Loan Servicing"),
    ("Other Consumer Lending", "Other Consumer Lending"),
    (
        "Other Consumer Products (Not Lending)",
        "Other Consumer Product (not lending)",
    ),
]

enforcement_at_risk_groups = [
    ("Fair Lending", "Fair Lending"),
    ("Limited English Proficiency", "Limited English Proficiency"),
    ("Older Americans", "Older Americans"),
    ("Servicemembers", "Servicemembers"),
    ("Students", "Students"),
]

enforcement_statutes = [
    (
        "CFPA Deceptive",
        "Consumer Financial Protection Act - Deceptive Acts or Practices",
    ),
    (
        "CFPA Unfair",
        "Consumer Financial Protection Act - Unfair Acts or Practices",
    ),
    (
        "CFPA Abusive",
        "Consumer Financial Protection Act - Abusive Acts or Practices",
    ),
    ("CFPA", "Consumer Financial Protection Act - Other"),
    ("AMTPA", "Alternative Mortgage Transaction Parity Act/Regulation D"),
    ("CLA", "Consumer Leasing Act/Regulation M"),
    ("Credit Practice Rules", "Credit Practices Rule"),
    ("EFTA/Regulation E", "Electronic Fund Transfer Act/Regulation E"),
    ("ECOA/Regulation B", "Equal Credit Opportunity Act/Regulation B"),
    ("FCBA", "Fair Credit Billing Act"),
    ("FCRA/Regulation V", "Fair Credit Reporting Act/Regulation V"),
    ("FDCPA", "Fair Debt Collection Practices Act/Regulation F"),
    ("FDIA", "Federal Deposit Insurance Act/Regulation I"),
    ("GLBA/Regulation P", "Gramm-Leach-Bliley Act/Regulation P"),
    ("HMDA", "Home Mortgage Disclosure Act/Regulation C"),
    ("HOEPA", "Home Ownership and Equity Protection Act"),
    ("HOPA", "Home Owners Protection Act"),
    (
        "ILSFDA",
        "Interstate Land Sales Full Disclosure Act/Regulation J, K, and L",
    ),
    ("Military Lending Act", "Military Lending Act"),
    (
        "Regulation N (MAP Rule)",
        "Mortgage Acts and Practices – Advertising Final Rule (Regulation N)",
    ),
    (
        "Regulation O (MARS Rule)",
        "Mortgage Assistance Relief Services Rule (Regulation O)",
    ),
    ("MRAPLA", "Mortgage Reform and Anti-Predatory Lending Act"),
    ("RESPA", "Real Estate Settlement Procedures Act/Regulation X"),
    ("SMLA", "S.A.F.E. Mortgage Licensing Act/Regulation H"),
    ("Telemarketing Sales Rule (TSR)", "Telemarketing Sales Rule"),
    ("TILA/Regulation Z", "Truth in Lending Act/Regulation Z"),
    ("TISA/Regulation DD", "Truth in Savings Act/Regulation DD"),
]


def decimal_field():
    return models.DecimalField(decimal_places=2, max_digits=13, default=0)


class EnforcementActionDisposition(models.Model):
    final_disposition = models.CharField(max_length=150, blank=True)
    final_disposition_type = models.CharField(
        max_length=15,
        choices=[("Final Order", "Final Order"), ("Dismissal", "Dismissal")],
        blank=True,
    )
    final_order_date = models.DateField(null=True, blank=True)
    dismissal_date = models.DateField(null=True, blank=True)
    final_order_consumer_redress = decimal_field()
    final_order_consumer_redress_suspended = decimal_field()
    final_order_other_consumer_relief = decimal_field()
    final_order_other_consumer_relief_suspended = decimal_field()
    final_order_disgorgement = decimal_field()
    final_order_disgorgement_suspended = decimal_field()
    final_order_civil_money_penalty = decimal_field()
    final_order_civil_money_penalty_suspended = decimal_field()
    estimated_consumers_entitled_to_relief = models.CharField(max_length=30, blank=True)

    action = ParentalKey(
        "v1.EnforcementActionPage",
        on_delete=models.CASCADE,
        related_name="enforcement_dispositions",
    )


class EnforcementActionStatus(models.Model):
    status = models.CharField(max_length=50, choices=enforcement_statuses)
    action = ParentalKey(
        "v1.EnforcementActionPage",
        on_delete=models.CASCADE,
        related_name="statuses",
    )


class EnforcementActionDocket(models.Model):
    docket_number = models.CharField(max_length=50)
    action = ParentalKey(
        "v1.EnforcementActionPage",
        on_delete=models.CASCADE,
        related_name="docket_numbers",
    )


class EnforcementActionDefendantType(models.Model):
    defendant_type = models.CharField(
        max_length=15, choices=enforcement_defendant_types, blank=True
    )
    action = ParentalKey(
        "v1.EnforcementActionPage",
        on_delete=models.CASCADE,
        related_name="defendant_types",
    )


class EnforcementActionProduct(models.Model):
    product = models.CharField(max_length=50, choices=enforcement_products)
    action = ParentalKey(
        "v1.EnforcementActionPage",
        on_delete=models.CASCADE,
        related_name="products",
    )


class EnforcementActionAtRisk(models.Model):
    at_risk_group = models.CharField(max_length=30, choices=enforcement_at_risk_groups)
    action = ParentalKey(
        "v1.EnforcementActionPage",
        on_delete=models.CASCADE,
        related_name="at_risk_groups",
    )


class EnforcementActionStatute(models.Model):
    statute = models.CharField(max_length=30, choices=enforcement_statutes)
    action = ParentalKey(
        "v1.EnforcementActionPage",
        on_delete=models.CASCADE,
        related_name="statutes",
    )


class EnforcementActionPage(AbstractFilterPage):
    public_enforcement_action = models.CharField(max_length=150, blank=True)
    initial_filing_date = models.DateField(null=True, blank=True)
    settled_or_contested_at_filing = models.CharField(
        max_length=10,
        choices=[("Settled", "Settled"), ("Contested", "Contested")],
        blank=True,
    )
    court = models.CharField(default="", max_length=150, blank=True)

    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("expandable", organisms.Expandable()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("notification", molecules.Notification()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("feedback", v1_blocks.Feedback()),
        ],
        blank=True,
    )

    content_panels = [StreamFieldPanel("header"), StreamFieldPanel("content")]

    metadata_panels = [
        FieldPanel("public_enforcement_action"),
        FieldPanel("initial_filing_date"),
        InlinePanel("defendant_types", label="Defendant/Respondent Type"),
        InlinePanel("categories", label="Forum", min_num=1, max_num=2),
        FieldPanel("court"),
        InlinePanel("docket_numbers", label="Docket Number", min_num=1),
        FieldPanel("settled_or_contested_at_filing"),
        InlinePanel("statuses", label="Status", min_num=1),
        InlinePanel("products", label="Products"),
        InlinePanel("at_risk_groups", label="At Risk Groups"),
        InlinePanel("statutes", label="Statutes/Regulations"),
        InlinePanel("enforcement_dispositions", label="Final Disposition"),
    ]

    settings_panels = [
        MultiFieldPanel(CFGOVPage.promote_panels, "Settings"),
        MultiFieldPanel(
            [
                FieldPanel("preview_title"),
                FieldPanel("preview_subheading"),
                FieldPanel("preview_description"),
                FieldPanel("secondary_link_url"),
                FieldPanel("secondary_link_text"),
                ImageChooserPanel("preview_image"),
            ],
            heading="Page Preview Fields",
            classname="collapsible",
        ),
        FieldPanel("authors", "Authors"),
        MultiFieldPanel(
            [
                FieldPanel("date_published"),
                FieldPanel("comments_close_by"),
            ],
            "Relevant Dates",
            classname="collapsible",
        ),
        MultiFieldPanel(Page.settings_panels, "Scheduled Publishing"),
        FieldPanel("language", "Language"),
        MultiFieldPanel(CFGOVPage.archive_panels, "Archive"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(
                AbstractFilterPage.content_panels + content_panels,
                heading="General Content",
            ),
            ObjectList(metadata_panels, heading="Metadata"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(settings_panels, heading="Configuration"),
        ]
    )

    template = "enforcement-action/index.html"

    objects = PageManager()

    search_fields = AbstractFilterPage.search_fields + [index.SearchField("content")]

    def get_context(self, request):
        context = super().get_context(request)
        dispositions = self.enforcement_dispositions.all()

        context.update(
            {
                "total_consumer_relief": sum(
                    disp.final_order_consumer_redress
                    + disp.final_order_other_consumer_relief
                    for disp in dispositions
                ),
                "total_cmp": sum(
                    disp.final_order_civil_money_penalty for disp in dispositions
                ),
                "defendant_types": [
                    d.get_defendant_type_display() for d in self.defendant_types.all()
                ],
                "statutes": [s.statute for s in self.statutes.all()],
                "products": [p.get_product_display() for p in self.products.all()],
                "at_risk_groups": [g.at_risk_group for g in self.at_risk_groups.all()],
            }
        )

        return context
