from wagtail.wagtailcore import blocks


class Hyperlink(blocks.StructBlock):
    label = blocks.CharBlock(max_length=50)
    href = blocks.CharBlock(default='/')
