from wagtail.wagtailcore import blocks
from v1.atomic_elements import organisms


class Tip(blocks.StructBlock):
    content = blocks.RichTextBlock(
                features=[
                        'link', 'document-link'
                    ],
                label='Tip')
    class Meta:
        icon = 'title'
        template = '_includes/ask/tip.html'


class AskAnswerContent(blocks.StreamBlock):
    text = blocks.StructBlock([
            ('content', blocks.RichTextBlock(
                features=[
                    'bold', 'italic', 'h2', 'h3', 'link', 'ol', 'ul',
                    'document-link', 'image', 'embed', 'edit-html'
                ],
            label='Text'
            ))
        ])
    table_block = organisms.AtomicTableBlock(
                    table_options={'renderer': 'html'})
    tip = Tip()
    video_player = organisms.VideoPlayer()

    class Meta:
        template = '_includes/ask/content-block.html'
