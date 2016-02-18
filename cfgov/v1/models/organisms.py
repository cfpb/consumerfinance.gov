from wagtail.wagtailcore import blocks
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock

from . import atoms, molecules, ref
from .snippets import Contact as ContactSnippetClass


class Well(blocks.StructBlock):
    content = blocks.RichTextBlock(required=False, label='Well')

    class Meta:
        icon = 'title'
        template = '_includes/organisms/well.html'


class ImageText5050Group(blocks.StructBlock):
    heading = blocks.CharBlock(icon='title', required=False)
    image_texts = blocks.ListBlock(molecules.ImageText5050())

    class Meta:
        icon = 'image'
        template = '_includes/organisms/image-text-50-50-group.html'


class ImageText2575Group(blocks.StructBlock):
    heading = blocks.CharBlock(icon='title', required=False)
    image_texts = blocks.ListBlock(molecules.ImageText2575())

    class Meta:
        icon = 'image'
        template = '_includes/organisms/image-text-25-75-group.html'


class HalfWidthLinkBlobGroup(blocks.StructBlock):
    heading = blocks.CharBlock(icon='title', required=False)
    link_blobs = blocks.ListBlock(molecules.HalfWidthLinkBlob())

    class Meta:
        icon = 'link'
        template = '_includes/organisms/half-width-link-blob-group.html'


class PostPreview(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    image = atoms.ImageBasic(required=False)

    post = blocks.PageChooserBlock(required=False)

    link = atoms.Hyperlink(required=False)

    class Meta:
        icon = 'view'
        template = '_includes/organisms/post-preview.html'


class PostPreviewSnapshot(blocks.StructBlock):
    limit = blocks.CharBlock(default='3', label='Limit',
                             help_text='How many posts do you want to show?')

    class Meta:
        icon = 'order'


class EmailSignUp(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    gd_code = blocks.CharBlock(required=False)

    form_field = blocks.ListBlock(molecules.FormFieldWithButton(), icon='mail', required=False)

    class Meta:
        icon = 'mail'
        template = '_includes/organisms/email-signup.html'


class RelatedPosts(blocks.StructBlock):
    limit = blocks.CharBlock(default='3', label='Limit')
    show_heading = blocks.BooleanBlock(required=False, default=True,
                                       label='Show Heading and Icon?',
                                       help_text='This toggles the heading and'
                                                 + ' icon for the related types.')
    relate_posts = blocks.BooleanBlock(required=False, default=True,
                                       label='Blog Posts', editable=False)
    relate_newsroom = blocks.BooleanBlock(required=False, default=True,
                                          label='Newsroom', editable=False)
    relate_events = blocks.BooleanBlock(required=False, default=True,
                                        label='Events')
    view_more = atoms.Hyperlink(required=False)

    class Meta:
        icon = 'link'
        template = '_includes/molecules/related-posts.html'


class MainContactInfo(blocks.StructBlock):
    header = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    contact = SnippetChooserBlock(ContactSnippetClass)

    class Meta:
        icon = 'wagtail'
        template = '_includes/organisms/main-contact-info.html'


class SidebarContactInfo(blocks.StructBlock):
    header = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    contact = SnippetChooserBlock(ContactSnippetClass)

    class Meta:
        icon = 'wagtail'
        template = '_includes/organisms/sidebar-contact-info.html'


class Table(blocks.StructBlock):
    headers = blocks.ListBlock(blocks.CharBlock())
    rows = blocks.ListBlock(blocks.StreamBlock([
        ('hyperlink', atoms.Hyperlink(required=False)),
        ('text', blocks.CharBlock()),
        ('text_blob', blocks.TextBlock()),
        ('rich_text_blob', blocks.RichTextBlock()),
    ]))

    class Meta:
        icon = 'form'
        template = '_includes/organisms/table.html'
        label = 'Table'


class FullWidthText(blocks.StreamBlock):
    content = blocks.RichTextBlock(icon='edit')
    quote = molecules.Quote()
    cta = molecules.CallToAction()
    related_links = molecules.RelatedLinks()
    table = Table()

    class Meta:
        icon = 'edit'
        template = '_includes/organisms/full-width-text.html'


class ExpandableGroup(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)

    is_accordion = blocks.BooleanBlock(required=False)
    has_rule = blocks.BooleanBlock(required=False)

    expandables = blocks.ListBlock(molecules.Expandable())

    class Meta:
        icon = 'list-ul'
        template = '_includes/organisms/expandable-group.html'

    class Media:
        js = ("expandable-group.js",)


class ItemIntroduction(blocks.StructBlock):
    category = blocks.ChoiceBlock(choices=ref.categories, required=False)

    heading = blocks.CharBlock(required=False)
    paragraph = blocks.RichTextBlock(required=False)

    authors = blocks.ListBlock(atoms.Hyperlink(required=False))
    date = blocks.DateTimeBlock(required=False)
    has_social = blocks.BooleanBlock(required=False, help_text="Whether to show the share icons or not.")

    class Meta:
        icon = 'form'
        template = '_includes/organisms/item-introduction.html'


class FilterControls(molecules.BaseExpandable):
    form_type = blocks.ChoiceBlock(choices=[
        ('filterable-list', 'Filterable List'),
        ('pdf-generator', 'PDF Generator'),
    ], default='filterable-list')
    title = blocks.BooleanBlock(default=True, required=False,
                                label='Filter Title')
    categories = blocks.StructBlock([
        ('filter_category', blocks.BooleanBlock(default=True, required=False)),
        ('page_type', blocks.ChoiceBlock(choices=ref.page_types,
                                         required=False)),
    ])
    topics = blocks.BooleanBlock(default=True, required=False,
                                 label='Filter Topics')
    authors = blocks.BooleanBlock(default=True, required=False,
                                  label='Filter Authors')
    date_range = blocks.BooleanBlock(default=True, required=False,
                                     label='Filter Date Range')

    class Meta:
        label = 'Filter Controls'
        icon = 'form'

    class Media:
        js = ('notification.js', 'expandable.js')
