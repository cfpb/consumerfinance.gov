###########################################################
# This is a test page containing all elements used on the
# frontend in Wagtail. This file can be used to run
# frontend tests on a dynamically created page. When
# adding new fields to wagtail pages, be sure to add them
# here as well and add corresponding tests.
###########################################################

from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.http import http_date

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from localflavor.us.models import USStateField
from modelcluster.fields import ParentalKey

from data_research.blocks import (
    ConferenceRegistrationForm,
    MortgageDataDownloads,
)
from jobmanager.blocks import JobListingList, JobListingTable
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms, schema
from v1.models.base import CFGOVPage
from v1.models.filterable_list_mixins import (
    CategoryFilterableMixin,
    FilterableListMixin,
)
from v1.models.home_page import image_alt_value_passthrough, image_passthrough
from v1.models.learn_page import AgendaItemBlock
from v1.util.events import get_venue_coords
from v1.util.util import get_secondary_nav_items
from youth_employment.blocks import YESChecklist


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
        "Mortgage Acts and Practices - Advertising Final Rule (Regulation N)",
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


class TestEnforcementActionDisposition(models.Model):
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
    estimated_consumers_entitled_to_relief = models.CharField(
        max_length=30, blank=True
    )

    action = ParentalKey(
        "v1.TestPage",
        on_delete=models.CASCADE,
        related_name="enforcement_dispositions",
    )


class TestEnforcementActionStatus(models.Model):
    status = models.CharField(max_length=50, choices=enforcement_statuses)
    action = ParentalKey(
        "v1.TestPage",
        on_delete=models.CASCADE,
        related_name="statuses",
    )


class TestEnforcementActionDocket(models.Model):
    docket_number = models.CharField(max_length=50)
    action = ParentalKey(
        "v1.TestPage",
        on_delete=models.CASCADE,
        related_name="docket_numbers",
    )


class TestEnforcementActionDefendantType(models.Model):
    defendant_type = models.CharField(
        max_length=15, choices=enforcement_defendant_types, blank=True
    )
    action = ParentalKey(
        "v1.TestPage",
        on_delete=models.CASCADE,
        related_name="defendant_types",
    )


class TestEnforcementActionProduct(models.Model):
    product = models.CharField(max_length=50, choices=enforcement_products)
    action = ParentalKey(
        "v1.TestPage",
        on_delete=models.CASCADE,
        related_name="products",
    )


class TestEnforcementActionAtRisk(models.Model):
    at_risk_group = models.CharField(
        max_length=30, choices=enforcement_at_risk_groups
    )
    action = ParentalKey(
        "v1.TestPage",
        on_delete=models.CASCADE,
        related_name="at_risk_groups",
    )


class TestEnforcementActionStatute(models.Model):
    statute = models.CharField(max_length=30, choices=enforcement_statutes)
    action = ParentalKey(
        "v1.TestPage",
        on_delete=models.CASCADE,
        related_name="statutes",
    )


class TestPage(FilterableListMixin, CategoryFilterableMixin, CFGOVPage):
    header = StreamField(
        [
            ("hero", molecules.Hero()),
            ("article_subheader", blocks.RichTextBlock(icon="form")),
            ("text_introduction", molecules.TextIntroduction()),
            ("item_introduction", organisms.ItemIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
            ("notification", molecules.Notification()),
            ("jumbo_hero", molecules.JumboHero()),
            ("features", organisms.InfoUnitGroup()),
        ],
        blank=True,
    )

    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_subheading = models.CharField(
        max_length=255, null=True, blank=True
    )
    preview_description = RichTextField(null=True, blank=True)
    secondary_link_url = models.CharField(
        max_length=500, null=True, blank=True
    )
    secondary_link_text = models.CharField(
        max_length=255, null=True, blank=True
    )
    preview_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    date_published = models.DateField(default=date.today)
    date_filed = models.DateField(null=True, blank=True)
    comments_close_by = models.DateField(null=True, blank=True)
    public_enforcement_action = models.CharField(max_length=150, blank=True)
    initial_filing_date = models.DateField(null=True, blank=True)
    settled_or_contested_at_filing = models.CharField(
        max_length=10,
        choices=[("Settled", "Settled"), ("Contested", "Contested")],
        blank=True,
    )
    court = models.CharField(default="", max_length=150, blank=True)

    # Event page elements. This is basically its own page within the test page
    body = RichTextField("Subheading", blank=True)
    archive_body = RichTextField(blank=True)
    live_body = RichTextField(blank=True)
    future_body = RichTextField(blank=True)
    persistent_body = StreamField(
        [
            ("content", blocks.RichTextBlock(icon="edit")),
            ("content_with_anchor", molecules.ContentWithAnchor()),
            ("heading", v1_blocks.HeadingBlock(required=False)),
            ("image", molecules.ContentImage()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            (
                "reusable_text",
                v1_blocks.ReusableTextChooserBlock("v1.ReusableText"),
            ),
        ],
        blank=True,
    )
    start_dt = models.DateTimeField("Start")
    end_dt = models.DateTimeField("End", blank=True, null=True)
    future_body = RichTextField(blank=True)
    archive_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    video_transcript = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    speech_transcript = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    flickr_url = models.URLField("Flickr URL", blank=True)
    archive_video_id = models.CharField(
        "YouTube video ID (archive)",
        null=True,
        blank=True,
        max_length=11,
        # This is a reasonable but not official regex for YouTube video IDs.
        # https://webapps.stackexchange.com/a/54448
        validators=[RegexValidator(regex=r"^[\w-]{11}$")],
        help_text=organisms.VideoPlayer.YOUTUBE_ID_HELP_TEXT,
    )
    live_stream_availability = models.BooleanField(
        "Streaming?",
        default=False,
        blank=True,
        help_text="Check if this event will be streamed live. This causes the "
        "event page to show the parts necessary for live streaming.",
    )
    live_video_id = models.CharField(
        "YouTube video ID (live)",
        null=True,
        blank=True,
        max_length=11,
        # This is a reasonable but not official regex for YouTube video IDs.
        # https://webapps.stackexchange.com/a/54448
        validators=[RegexValidator(regex=r"^[\w-]{11}$")],
        help_text=organisms.VideoPlayer.YOUTUBE_ID_HELP_TEXT,
    )
    live_stream_date = models.DateTimeField(
        "Go Live Date",
        blank=True,
        null=True,
        help_text="Enter the date and time that the page should switch from "
        "showing the venue image to showing the live video feed. "
        "This is typically 15 minutes prior to the event start time.",
    )

    # Venue content fields
    venue_coords = models.CharField(max_length=100, blank=True)
    venue_name = models.CharField(max_length=100, blank=True)
    venue_street = models.CharField(max_length=100, blank=True)
    venue_suite = models.CharField(max_length=100, blank=True)
    venue_city = models.CharField(max_length=100, blank=True)
    venue_state = USStateField(blank=True)
    venue_zipcode = models.CharField(max_length=12, blank=True)
    venue_image_type = models.CharField(
        max_length=8,
        choices=(
            ("map", "Map"),
            ("image", "Image (selected below)"),
            ("none", "No map or image"),
        ),
        default="map",
        help_text='If "Image" is chosen here, you must select the image you '
        "want below. It should be sized to 1416x796.",
    )
    venue_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    post_event_image_type = models.CharField(
        max_length=16,
        choices=(
            ("placeholder", "Placeholder image"),
            ("image", "Unique image (selected below)"),
        ),
        default="placeholder",
        verbose_name="Post-event image type",
        help_text="Choose what to display after an event concludes. This will "
        'be overridden by embedded video if the "YouTube video ID '
        '(archive)" field on the previous tab is populated. If '
        '"Unique image" is chosen here, you must select the image '
        "you want below. It should be sized to 1416x796.",
    )
    post_event_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Agenda content fields
    agenda_items = StreamField([("item", AgendaItemBlock())], blank=True)
    # End of event page content

    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("info_units", organisms.InfoUnitGroup()),
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("text_introduction", molecules.TextIntroduction()),
            ("simple_chart", organisms.SimpleChart()),
            ("expandable", organisms.Expandable()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("contact", organisms.MainContactInfo()),
            ("contact_expandable_group", organisms.ContactExpandableGroup()),
            ("featured_content", organisms.FeaturedContent()),
            ("notification", molecules.Notification()),
            ("well", organisms.Well()),
            ("call_to_action", molecules.CallToAction()),
            ("image", molecules.ContentImage()),
            ("video_player", organisms.VideoPlayer()),
            ("snippet_list", organisms.ResourceList()),
            ("post_preview_snapshot", organisms.PostPreviewSnapshot()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("email_signup", organisms.EmailSignUp()),
            ("audio_player", organisms.AudioPlayer()),
            ("filter_controls", organisms.FilterableList()),
            ("feedback", v1_blocks.Feedback()),
            ("faq_schema", schema.FAQ(label="FAQ schema")),
            ("how_to_schema", schema.HowTo(label="HowTo schema")),
            ("raw_html_block", blocks.RawHTMLBlock(label="Raw HTML block")),
            ("conference_registration_form", ConferenceRegistrationForm()),
            ("chart_block", organisms.ChartBlock()),
            ("mortgage_chart_block", organisms.MortgageChartBlock()),
            ("mortgage_map_block", organisms.MortgageMapBlock()),
            ("mortgage_downloads_block", MortgageDataDownloads()),
            ("data_snapshot", organisms.DataSnapshot()),
            ("job_listing_table", JobListingTable()),
            ("yes_checklist", YESChecklist()),
            ("erap_tool", v1_blocks.RAFToolBlock()),
            ("raf_tool", v1_blocks.RAFTBlock()),
        ],
        blank=True,
    )

    sidebar_breakout = StreamField(
        [
            ("slug", blocks.CharBlock(icon="title")),
            ("heading", blocks.CharBlock(icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="edit")),
            (
                "breakout_image",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock()),
                        (
                            "is_round",
                            blocks.BooleanBlock(
                                required=False, default=True, label="Round?"
                            ),
                        ),
                        (
                            "icon",
                            blocks.CharBlock(
                                help_text="Enter icon class name."
                            ),
                        ),
                        (
                            "heading",
                            blocks.CharBlock(
                                required=False, label="Introduction Heading"
                            ),
                        ),
                        (
                            "body",
                            blocks.TextBlock(
                                required=False, label="Introduction Body"
                            ),
                        ),
                    ],
                    heading="Breakout Image",
                    icon="image",
                ),
            ),
            ("related_posts", organisms.RelatedPosts()),
            ("job_listing_list", JobListingList()),
        ],
        blank=True,
    )

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    share_and_print = models.BooleanField(
        default=False,
        help_text="Include share and print buttons above page content.",
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        FieldPanel("share_and_print"),
        StreamFieldPanel("content"),
        FieldPanel("body"),
        FieldRowPanel(
            [
                FieldPanel("start_dt", classname="col6"),
                FieldPanel("end_dt", classname="col6"),
            ]
        ),
        MultiFieldPanel(
            [
                FieldPanel("archive_body"),
                ImageChooserPanel("archive_image"),
                DocumentChooserPanel("video_transcript"),
                DocumentChooserPanel("speech_transcript"),
                FieldPanel("flickr_url"),
                FieldPanel("archive_video_id"),
            ],
            heading="Archive Information",
        ),
        FieldPanel("live_body"),
        FieldPanel("future_body"),
        StreamFieldPanel("persistent_body"),
        MultiFieldPanel(
            [
                FieldPanel("live_stream_availability"),
                FieldPanel("live_video_id"),
                FieldPanel("live_stream_date"),
            ],
            heading="Live Stream Information",
        ),
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel("secondary_nav_exclude_sibling_pages"),
        StreamFieldPanel("sidebar_breakout"),
    ]

    # Venue content tab
    venue_panels = [
        FieldPanel("venue_name"),
        MultiFieldPanel(
            [
                FieldPanel("venue_street"),
                FieldPanel("venue_suite"),
                FieldPanel("venue_city"),
                FieldPanel("venue_state"),
                FieldPanel("venue_zipcode"),
            ],
            heading="Venue Address",
        ),
        MultiFieldPanel(
            [
                FieldPanel("venue_image_type"),
                ImageChooserPanel("venue_image"),
            ],
            heading="Venue Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("post_event_image_type"),
                ImageChooserPanel("post_event_image"),
            ],
            heading="Post-event Image",
        ),
    ]

    # Agenda content tab
    agenda_panels = [
        StreamFieldPanel("agenda_items"),
    ]

    # Promotion panels
    promote_panels = [
        MultiFieldPanel(CFGOVPage.promote_panels, "Page configuration"),
    ]

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
        InlinePanel("categories", label="Categories", max_num=2),
        FieldPanel("tags", "Tags"),
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
        FieldPanel("schema_json", "Structured Data"),
        FieldPanel("authors", "Authors"),
        FieldPanel("content_owners", "Content Owners"),
        MultiFieldPanel(
            [
                FieldPanel("date_published"),
                FieldPanel("date_filed"),
                FieldPanel("comments_close_by"),
            ],
            "Relevant Dates",
            classname="collapsible",
        ),
        MultiFieldPanel(Page.settings_panels, "Scheduled Publishing"),
        FieldPanel("language", "Language"),
        MultiFieldPanel(CFGOVPage.archive_panels, "Archive"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(sidefoot_panels, heading="Sidefoot"),
            ObjectList(settings_panels, heading="Configuration"),
            ObjectList(metadata_panels, heading="Metadata"),
            ObjectList(venue_panels, heading="Venue Information"),
            ObjectList(agenda_panels, heading="Agenda Information"),
        ]
    )

    template = "test-page/index.html"

    search_fields = CFGOVPage.search_fields + [
        index.SearchField("body"),
        index.SearchField("archive_body"),
        index.SearchField("live_video_id"),
        index.SearchField("flickr_url"),
        index.SearchField("archive_video_id"),
        index.SearchField("future_body"),
        index.SearchField("agenda_items"),
        index.SearchField("content"),
        index.SearchField("header"),
    ]

    filterable_categories = ("Blog", "Newsroom", "Research Report")
    filterable_per_page_limit = 100

    @property
    def event_state(self):
        if self.end_dt and self.end_dt < self._cached_now:
            return "past"

        start = min(filter(None, [self.live_stream_date, self.start_dt]))
        if self._cached_now >= start:
            return "present"

        return "future"

    @property
    def page_js(self):
        if (self.live_stream_date and self.event_state == "present") or (
            self.archive_video_id and self.event_state == "past"
        ):
            return (
                super().page_js
                + ["video-player.js"]
                + ["secondary-navigation.js"]
            )

        return super().page_js + ["secondary-navigation.js"]

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        parent_meta = super().meta_image
        return parent_meta or self.preview_image

    def location_image_url(self, scale="2", size="276x155", zoom="12"):
        if not self.venue_coords:
            self.venue_coords = get_venue_coords(
                self.venue_city, self.venue_state
            )
        api_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"
        static_map_image_url = "{}/{},{}/{}?access_token={}".format(
            api_url,
            self.venue_coords,
            zoom,
            size,
            settings.MAPBOX_ACCESS_TOKEN,
        )

        return static_map_image_url

    def clean(self):
        super().clean()
        if self.venue_image_type == "image" and not self.venue_image:
            raise ValidationError(
                {"venue_image": 'Required if "Venue image type" is "Image".'}
            )
        if self.post_event_image_type == "image" and not self.post_event_image:
            raise ValidationError(
                {
                    "post_event_image": 'Required if "Post-event image type" is '
                    '"Image".'
                }
            )
        if self.live_stream_availability:
            if not self.live_stream_date:
                self.live_stream_date = self.start_dt
            # Make sure live stream doesn't start after event end.
            if self.end_dt and self.live_stream_date >= self.end_dt:
                raise ValidationError(
                    {"live_stream_date": "Cannot be on or after Event End."}
                )

    def save(self, *args, **kwargs):
        self.venue_coords = get_venue_coords(self.venue_city, self.venue_state)
        return super().save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["event_state"] = self.event_state
        dispositions = self.enforcement_dispositions.all()

        context.update(
            {
                "total_consumer_relief": sum(
                    disp.final_order_consumer_redress
                    + disp.final_order_other_consumer_relief
                    for disp in dispositions
                ),
                "total_cmp": sum(
                    disp.final_order_civil_money_penalty
                    for disp in dispositions
                ),
                "defendant_types": [
                    d.get_defendant_type_display()
                    for d in self.defendant_types.all()
                ],
                "statutes": [s.statute for s in self.statutes.all()],
                "products": [
                    p.get_product_display() for p in self.products.all()
                ],
                "at_risk_groups": [
                    g.at_risk_group for g in self.at_risk_groups.all()
                ],
                "get_secondary_nav_items": get_secondary_nav_items,
                "image_passthrough": image_passthrough,
                "image_alt_value_passthrough": image_alt_value_passthrough,
            }
        )

        return context

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)

        changes_at = [self.start_dt, self.end_dt, self.live_stream_date]
        future_changes_at = [
            at for at in changes_at if at and at > self._cached_now
        ]

        if future_changes_at:
            response["Expires"] = http_date(min(future_changes_at).timestamp())

        return response

    def get_browsefilterable_posts(self, limit):
        posts_list = []

        return sorted(
            posts_list, key=lambda p: p.date_published, reverse=True
        )[:limit]

    @cached_property
    def _cached_now(self):
        """Cached value of now for use during page rendering.

        This property can be used to retrieve a fixed version of "now"
        associated with a single EventPage instance. The first time this
        property is accessed, it will return the current time. Any subsequent
        accesses will return the same time.

        This allows for a consistent timestamp to be used during page render.
        """
        return timezone.now()
