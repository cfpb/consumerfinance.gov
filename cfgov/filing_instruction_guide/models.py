import json
from datetime import date

from django import forms
from django.db import models

from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
    TitleFieldPanel,
)
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField

import requests
from modelcluster.models import ClusterableModel

from filing_instruction_guide import import_data_points
from filing_instruction_guide.blocks import (
    FigLevel3Subsection,
    FigSection,
    FigSubsection,
    content_block_options,
)
from v1.models.base import CFGOVPage


class FIGPageForm(WagtailAdminPageForm):
    def clean(self):
        data = super().clean()
        field = "data_points_download_location"
        try:
            import_data_points.run(data, self.instance)
        except KeyError as err:
            msg = f"""
            The JSON file provided does not match the expected format.
            Missing key: {err}
            """
            self.add_error(field, forms.ValidationError(msg))
        except (json.JSONDecodeError, requests.exceptions.JSONDecodeError):
            msg = """
            Unable to parse the input file as JSON.
            Please check that the file uses valid JSON.
            """
            self.add_error(field, forms.ValidationError(msg))
        except requests.exceptions.RequestException:
            msg = """
            The file could not be downloaded at the specified URL.
            """
            self.add_error(field, forms.ValidationError(msg))
        return data

    # Upon saving or previewing the page, assign section IDs
    def save(self, commit=True):
        page = super().save(commit=False)
        page.assign_section_ids()
        if commit:
            page.save()
        return page


class FIGContentPage(CFGOVPage, ClusterableModel):
    # FIG Header Section Fields
    eyebrow = models.CharField(max_length=100, blank=True)
    page_header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)

    # FIG Version fields
    version_status = models.CharField(
        choices=[
            ("current", "Current"),
            ("old", "Out-of-date"),
            ("archived", "Archived"),
        ],
        default="current",
        max_length=20,
    )
    effective_start_date = models.DateField(
        blank=True, null=True, default=date.today
    )
    effective_end_date = models.DateField(blank=True, null=True)

    top_content = StreamField(
        [
            (
                "top_content",
                StreamBlock(
                    content_block_options,
                    required=False,
                    help_text="Content that will appear above the first FIG section",  # noqa: E501
                ),
            )
        ],
        blank=True,
    )

    content = StreamField(
        [
            ("Fig_Section", FigSection()),
            ("Fig_Subsection", FigSubsection()),
            ("Fig_Level_3_Subsection", FigLevel3Subsection()),
        ],
    )

    # Main content panel
    content_panels = [
        MultiFieldPanel(
            [
                TitleFieldPanel("title"),
            ],
            heading="Page Title",
        ),
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("page_header"),
                FieldPanel("subheader"),
            ],
            heading="Filing Instruction Guide Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("version_status"),
                FieldPanel("effective_start_date"),
                FieldPanel("effective_end_date"),
            ],
            heading="FIG Version Information",
        ),
        FieldPanel("top_content"),
        FieldPanel("content"),
    ]

    # Data points panel
    data_points_download_location = models.CharField(
        max_length=300,
        blank=True,
        help_text=(
            "The URL of the raw JSON file containing the FIG data points"
        ),
    )
    data_points_panel = [
        MultiFieldPanel(
            [FieldPanel("data_points_download_location")],
            heading="Data Points",
        )
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(data_points_panel, heading="Data points"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    def get_toc_headers(self, request):
        toc_headers = []
        parent = None
        for section in self.content:
            header = section.value.get("header")
            id = section.value.get("section_id")
            if section.block_type == "Fig_Section":
                if parent:
                    toc_headers.append(parent)
                parent = {
                    "header": header,
                    "id": id,
                    "anchor": f"#{id}",
                    "children": [],
                }
                if any(
                    y.block_type == "data_points_block"
                    for y in section.value["content"]
                ):
                    # If a data_points_block is part of this section's
                    # contents, add the data points to the headers collection
                    for p in self.data_points.order_by("number"):
                        parent["children"].append(
                            {
                                "header": p.title,
                                "id": f"{id}.{p.number}",
                                "anchor": f"#{p.anchor}",
                            }
                        )
            elif section.block_type == "Fig_Subsection":
                # if the first block is a subsection instead of a section
                if not parent:
                    parent = {"header": "", "id": "", "children": []}
                parent["children"].append(
                    {"header": header, "id": id, "anchor": f"#{id}"}
                )
        toc_headers.append(parent)
        return toc_headers

    def assign_section_ids(self):
        ind = sub_ind = sub3_ind = 0
        for section in self.content:
            id = ""
            sec_type = section.block_type
            if sec_type == "Fig_Section":
                ind += 1
                sub_ind = 0
                sub3_ind = 0
                id = f"{ind}"
            if sec_type == "Fig_Subsection":
                sub_ind += 1
                sub3_ind = 0
                id = f"{ind}.{sub_ind}"
            if sec_type == "Fig_Level_3_Subsection":
                sub3_ind += 1
                id = f"{ind}.{sub_ind}.{sub3_ind}"
            section.value["section_id"] = id

    base_form_class = FIGPageForm
    template = "filing_instruction_guide/index.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({"toc_headers": self.get_toc_headers(request)})
        return context
