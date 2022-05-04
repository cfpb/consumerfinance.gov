from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField

from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


def get_sections(request, self):

        # def content2(section, header_label, object_label):
        #     items = ['content', 'image']
        #     for item in [header_label] + [items]:
        #         if item == header_label:
        #             return {"section_type": object_label, "data": section.value[header_label]}
        #         else:
        #             return {"section_type": "content", "data": section.value[item]}

        def get_content(section):
            if section.block_type == 'Fig_Section':
                return {"section_type": "main", "data": section.value['header']}
                # return content2(section, "header", "main")
            if section.block_type == 'Fig_Sub_Section':
                return {"section_type": "sub", "data": section.value['sub_section_header']}
            if section.block_type == 'Fig_Sub_3_Section':
                return {"section_type": "sub3", "data": section.value['sub_section3_header']}

        sections = [
            get_content(section)
            for section in self.content
        ]

        main_ind = sub_ind = sub3_ind  = 0

        for index, section in enumerate(sections):
            if section["section_type"] == "main":
                sub_ind = 0
                sub3_ind = 0
                main_ind += 1
                section["id"] = str(main_ind)

            if section["section_type"] == "sub":
                if sections[index - 1]["section_type"] == "main":
                    sub_ind += 1
                    section["id"] = str(main_ind) + '.' + str(sub_ind)

                if sections[index - 1]["section_type"] == "sub" or sections[index - 1]["section_type"] == "sub3":
                    sub3_ind = 0
                    sub_ind += 1
                    section["id"] = str(main_ind) + '.' + str(sub_ind)
            
            if section["section_type"] == "sub3":
                if sections[index - 1]["section_type"] == "sub":
                    sub3_ind = 0
                    sub3_ind += 1
                    section["id"] = str(main_ind) + '.' + str(sub_ind) + '.' + str(sub3_ind) 
                else:
                    sub3_ind += 1
                    section["id"] = str(main_ind) + '.' + str(sub_ind) + '.' + str(sub3_ind) 
 
        return sections

class FIGContentPage(CFGOVPage):

    # FIG Header Section Fields
    report_type = models.CharField(max_length=100, blank=True)
    page_header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)

    content = StreamField([
        ("Fig_Section", molecules.FigSection()),
        ("Fig_Sub_Section", organisms.FigSubSection()),
        ("Fig_Sub_3_Section", organisms.FigSub3Section()),

    ], blank=True)

    # Report upload tab
    content_panels = [

        MultiFieldPanel(
            [
                FieldPanel("title"),
            ],
            heading="Page Title",
        ),
        MultiFieldPanel(
            [
                FieldPanel("report_type"),
                FieldPanel("page_header"),
                FieldPanel("subheader"),
            ],
            heading="Filing Instruction Guide Header",
        ),

        StreamFieldPanel("content")
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(
                content_panels, heading="Filing Instruction Guide Content"
            ),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "filing_instruction_guide/index.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "get_sections": get_sections(request, self)
            }
        )
        return context
