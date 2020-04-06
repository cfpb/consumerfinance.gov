from wagtail.core import blocks


class YESChecklistItem(blocks.StructBlock):
    """Deliver a standard set of values for a checklist item."""

    item = blocks.CharBlock(
        help_text='Short description for a checkbox item')
    details = blocks.RichTextBlock(
        help_text='Deeper explanation of the item',
        required=False)

    class Meta:
        template = 'youth_employment/yes-checklist-items.html'


class YESChecklist(blocks.StructBlock):
    """Deliver a set of values for building a print checklist."""

    checklist = blocks.ListBlock(YESChecklistItem())

    class Meta:
        icon = 'list-ul'
        template = 'youth_employment/yes-checklist.html'
        label = 'Youth employment checklist'

    class Media:
        js = ["youth-employment-programs/buying-a-car/index.js"]
