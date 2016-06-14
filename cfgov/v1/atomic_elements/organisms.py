from wagtail.wagtailcore import blocks
from wagtail.wagtailimages import blocks as images_blocks
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock

from . import atoms, molecules
from ..util import ref
from ..models.snippets import Contact as ContactSnippetClass


class Well(blocks.StructBlock):
    content = blocks.RichTextBlock(required=False, label='Well')

    class Meta:
        icon = 'title'
        template = '_includes/organisms/well.html'
        classname = 'block__flush'


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


class PostPreviewSnapshot(blocks.StructBlock):
    limit = blocks.CharBlock(default='3', label='Limit',
                             help_text='How many posts do you want to show?')

    post_date_description = blocks.CharBlock(default='Published')

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


class RegComment(blocks.StructBlock):
    document_id = blocks.CharBlock(required=True, label='Document ID',
                                   help_text='Federal Register document ID number to which the comment should be submitted. Should follow this format: CFPB-YYYY-####-####')
    generic_regs_link = blocks.BooleanBlock(required=False, default=True,
                                            label='Use generic Regs.gov link?',
                                            help_text='If unchecked, the link to comment at Regulations.gov if you want to add attachments will link directly to the document given above. Leave this checked if this comment form is being published before the full document is live at Regulations.gov, then uncheck it when the full document has been published.')
    id = blocks.CharBlock(required=False, label='Form ID',
                          help_text='Sets the `id` attribute in the form\'s markup. If not set, the form will be assigned a base id of `o-reg-comment_` with a random number appended.')

    class Meta:
        icon = 'form'
        template = '_includes/organisms/reg-comment.html'


class RelatedPosts(blocks.StructBlock):
    limit = blocks.CharBlock(default='3', label='Limit')
    show_heading = blocks.BooleanBlock(required=False, default=True,
                                       label='Show Heading and Icon?',
                                       help_text='This toggles the heading and'
                                                 + ' icon for the related types.')
    header_title = blocks.CharBlock(default='Further reading', label='Slug Title')

    relate_posts = blocks.BooleanBlock(required=False, default=True,
                                       label='Blog Posts', editable=False)
    relate_newsroom = blocks.BooleanBlock(required=False, default=True,
                                          label='Newsroom', editable=False)
    relate_events = blocks.BooleanBlock(required=False, default=True,
                                        label='Events')

    specific_categories = blocks.ListBlock(blocks.ChoiceBlock(choices=ref.related_posts_categories, required=False), required=False)

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


class SidebarContactInfo(MainContactInfo):
    class Meta:
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
    media = images_blocks.ImageChooserBlock(icon='image')
    quote = molecules.Quote()
    cta = molecules.CallToAction()
    related_links = molecules.RelatedLinks()
    table = Table()

    class Meta:
        icon = 'edit'
        template = '_includes/organisms/full-width-text.html'


class BaseExpandable(blocks.StructBlock):
    label = blocks.CharBlock(required=False)
    is_bordered = blocks.BooleanBlock(required=False)
    is_midtone = blocks.BooleanBlock(required=False)
    is_expanded = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'list-ul'
        template = '_includes/organisms/expandable.html'
        label = 'Expandable'

    class Media:
        js = ["expandable.js"]


class Expandable(BaseExpandable):
    content = blocks.StreamBlock(
        [
            ('paragraph', blocks.RichTextBlock(required=False)),
            ('well', Well()),
            ('links', atoms.Hyperlink()),
            ('email', molecules.ContactEmail()),
            ('phone', molecules.ContactPhone()),
            ('address', molecules.ContactAddress()),
        ], blank=True
    )


class ExpandableGroup(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)

    is_accordion = blocks.BooleanBlock(required=False)
    has_rule = blocks.BooleanBlock(required=False)

    expandables = blocks.ListBlock(Expandable())

    class Meta:
        icon = 'list-ul'
        template = '_includes/organisms/expandable-group.html'

    class Media:
        js = ["expandable-group.js"]


class ItemIntroduction(blocks.StructBlock):
    category = blocks.ChoiceBlock(choices=ref.categories, required=False)

    heading = blocks.CharBlock(required=False)
    paragraph = blocks.RichTextBlock(required=False)

    date = blocks.DateBlock(required=False)
    has_social = blocks.BooleanBlock(required=False, help_text="Whether to show the share icons or not.")

    class Meta:
        icon = 'form'
        template = '_includes/organisms/item-introduction.html'
        classname = 'block__flush-top'


# TODO: FilterControls/Filterable List should be updated to use same
#       atomic name used on the frontend of FilterableListControls,
#       or vice versa.
class FilterControls(BaseExpandable):
    form_type = blocks.ChoiceBlock(choices=[
        ('filterable-list', 'Filterable List'),
        ('pdf-generator', 'PDF Generator'),
    ], default='filterable-list')
    title = blocks.BooleanBlock(default=True, required=False,
                                label='Filter Title')
    post_date_description = blocks.CharBlock(default='Published')
    categories = blocks.StructBlock([
        ('filter_category', blocks.BooleanBlock(default=True, required=False)),
        ('show_preview_categories', blocks.BooleanBlock(default=True, required=False)),
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
        js = ['filterable-list-controls.js']
