from wagtail.wagtailcore import blocks

class YESChecklistItem(blocks.StructBlock):
    """Deliver a standard set of values for a checklist item."""

    item = blocks.CharBlock(
        help_text= 'Short description for a checkbox item')
    details = blocks.TextBlock(
        help_text= 'Deeper explanation of the item')

    class Meta:
        template = 'youth_employment/_includes/molecules/yes-checklist-items.html'


class YESChecklist(blocks.StructBlock):
    """Deliver a set of values for building a print checklist."""

    checklist = blocks.ListBlock(YESChecklistItem())

    class Meta:
        icon = 'list-ul'
        template = 'youth_employment/_includes/molecules/yes-checklist.html'
        label = 'Youth employment checklist'
