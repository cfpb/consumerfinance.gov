from wagtail.core import hooks

from filing_instruction_guide.models import FIGContentPage


def assign_content_section_ids(request, page):
    if page.specific_class == FIGContentPage:
        page.assign_section_ids()


hooks.register("after_create_page", assign_content_section_ids)
hooks.register("after_edit_page", assign_content_section_ids)
