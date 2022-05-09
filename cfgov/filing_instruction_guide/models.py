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


# function passed to context processor 
def parse_section_builder(request, self):

    # creates section dictionary object
    def create_section_object(section, type_of_block):
        contents_list = []
        for key in section.value.keys():
            contents_list.append({"section_type": key, "data": str(section.value[key])})
        section_block_object = {'block_type': type_of_block, "contents": contents_list}
        return section_block_object
    
    # determines which section dictionary object to create
    def get_content(section):
        if section.block_type == 'Fig_Section':
            sections.append(create_section_object(section, 'Fig_Section'))
        if section.block_type == 'Fig_Sub_Section':
            sections.append(create_section_object(section, 'Fig_Sub_Section'))
        if section.block_type == 'Fig_Sub_3_Section':
            sections.append(create_section_object(section, 'Fig_Sub_3_Section'))

    sections = []

    for section in self.content:
        get_content(section)

    # instantiate section index variables
    main_ind = sub_ind = sub3_ind = 0

    # assign ids to every Fig Section, Fig Sub Section, and Fig Sub 3 Section
    for index, section in enumerate(sections):
        if section["block_type"] == "Fig_Section":
            sub_ind = 0
            sub3_ind = 0
            main_ind += 1
            section["id"] = str(main_ind)

        if section["block_type"] == "Fig_Sub_Section":
            if sections[index - 1]["block_type"] == "Fig_Section":
                sub_ind += 1
                section["id"] = str(main_ind) + '.' + str(sub_ind)

            if sections[index - 1]["block_type"] == "Fig_Sub_Section" or sections[index - 1]["block_type"] == "Fig_Sub_3_Section":
                sub3_ind = 0
                sub_ind += 1
                section["id"] = str(main_ind) + '.' + str(sub_ind)
        
        if section["block_type"] == "Fig_Sub_3_Section":
            if sections[index - 1]["block_type"] == "Fig_Sub_3_Section":
                sub3_ind = 0
                sub3_ind += 1
                section["id"] = str(main_ind) + '.' + str(sub_ind) + '.' + str(sub3_ind) 
            else:
                sub3_ind += 1
                section["id"] = str(main_ind) + '.' + str(sub_ind) + '.' + str(sub3_ind) 

    return sections


# Template page
class FIGContentPage(CFGOVPage):

    # FIG Header Section Fields
    report_type = models.CharField(max_length=100, blank=True)
    page_header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)

    # FIG Content Section Fields
    content = StreamField([
        ("Fig_Section", organisms.FigSection()),
        ("Fig_Sub_Section", organisms.FigSubSection()),
        ("Fig_Sub_3_Section", organisms.FigSub3Section()),

    ], blank=True)

    # Wagtail Content Panels
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

    # Context Processor that provides the context for the template
    # Note: 'context' is key/value pair that is sent ot the template for mapping
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "get_sections": parse_section_builder(request, self)
            }
        )
        return context
