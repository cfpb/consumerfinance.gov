
import json

from django import forms
from django.template.loader import render_to_string
from django.utils.functional import cached_property

from django.apps import apps
from django.utils.encoding import smart_text
from wagtail.contrib.table_block.blocks import TableBlock, TableInput
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages import blocks as images_blocks
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock


from . import atoms, molecules
from ..util import ref
from ..models.snippets import Contact as ContactSnippetClass

from jinja2 import Markup


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


class LinkBlobGroup(blocks.StructBlock):
    heading = blocks.CharBlock(icon='title', required=False)
    has_top_border = blocks.BooleanBlock(required=False)
    has_bottom_border = blocks.BooleanBlock(required=False)
    link_blobs = blocks.ListBlock(molecules.HalfWidthLinkBlob())


class ThirdWidthLinkBlobGroup(LinkBlobGroup):
    class Meta:
        icon = 'link'
        template = '_includes/organisms/third-width-link-blob-group.html'


class HalfWidthLinkBlobGroup(LinkBlobGroup):
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
        icon = None
        template = '_includes/organisms/table.html'
        label = ' '


class AtomicTableInput(TableInput):
    _id = 'table-block'

    def render(self, name, value, attrs=None):
        attrs.update({'id': self._id})

        # Calling the grandparents render method and bypassing TableInputs,
        # in order to control how we render the form.
        original_field_html = super(TableInput, self).render(
            name, value, attrs
        )

        return Markup(render_to_string('wagtailadmin/table_input.html', {
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
        }))

    def render_js_init(self, id_, name, value):
        return "initAtomicTable({0}, {1});".format(
            json.dumps(id_),
            json.dumps(self.table_options)
        )


class AtomicTableBlock(TableBlock):
    @cached_property
    def field(self):
        widget = AtomicTableInput(table_options=self.table_options)
        return forms.CharField(widget=widget, **self.field_options)

    class Meta:
        default = None
        icon = 'table'
        template = '_includes/organisms/table.html'


class ModelBlock(blocks.StructBlock):
    """Abstract StructBlock that provides Django model instances to subclasses.

    This class inherits from the standard Wagtail StructBlock but adds helper
    methods that allow subclasses to dynamically render Django model instances.
    This is useful if, for example, a widget needs to show a list of all model
    instances meeting a certain criteria.

    Subclasses must override the 'model' class attribute with the fully-
    qualified name of the model to be used, for example 'my.app.Modelname'.

    Subclasses may optionally override the 'filter_queryset' method to do
    filtering on the model QuerySet.

    Subclasses may optionally override either the class attributes 'ordering'
    (providing a Django-style string or tuple of orderings to use) and 'limit'
    (providing an integer to use to slice the model QuerySet), or provide
    methods 'get_ordering' and 'get_limit' that do the same thing.

    """
    model = None
    ordering = None
    limit = None

    def get_queryset(self, value):
        model_cls = apps.get_model(self.model)
        qs = model_cls.objects.all()

        qs = self.filter_queryset(qs, value)

        ordering = self.get_ordering(value)
        if ordering:
            if isinstance(ordering, basestring):
                ordering = (ordering,)

            qs = qs.order_by(*ordering)

        limit = self.get_limit(value)
        if limit:
            qs = qs[:limit]

        return qs

    def filter_queryset(self, qs, value):
        return qs

    def get_ordering(self, value):
        return self.ordering

    def get_limit(self, value):
        return self.limit


class ModelTable(ModelBlock):
    """Abstract StructBlock that can generate a table from a Django model.

    Subclasses must override the 'fields' and 'field_headers' class attributes
    to specify which model fields to include in the generated table.

    By default model instance values will be converted to text for display
    in table rows. To override this, subclasses may define custom field
    formatter methods, using the name 'make_FIELD_value'. This may be useful
    if fields are non-text types, for example when formatting dates.

    For example:

        def make_created_value(self, instance, value):
            return value.strftime('%b %d, %Y')

    """
    fields = None
    field_headers = None

    row_links = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text='Whether to highlight rows containing links'
    )

    def render(self, value):
        rows = [
            self.make_row(instance)
            for instance in self.get_queryset(value)
        ]

        table_value = {
            'headers': self.field_headers,
            'rows': rows,
            'row_links': value.get('row_links'),
        }

        table = Table()
        value = table.to_python(table_value)
        return table.render(value)

    def make_row(self, instance):
        return [
            {'type': 'text', 'value': self.make_value(instance, field)}
            for field in self.fields
        ]

    def make_value(self, instance, field):
        value = getattr(instance, field)
        return self.format_field_value(instance, field, value)

    def format_field_value(self, instance, field, value):
        custom_formatter_name = 'make_{}_value'.format(field)
        custom_formatter = getattr(self, custom_formatter_name, None)

        if custom_formatter:
            return custom_formatter(instance, value)
        else:
            return smart_text(value)

    class Meta:
        icon = 'table'


class ModelList(ModelBlock):
    """Abstract StructBlock that can generate a list from a Django model.

    Subclasses must define a 'render' method that renders the model QuerySet
    to a string.

    For example:

        def render(self, value):
            value['objects'] = self.get_queryset(value)
            template = 'path/to/template.html'
            return render_to_string(template, value)

    """
    limit = atoms.IntegerBlock(
        default=5,
        label='Maximum items',
        min_value=0,
        help_text='Limit list to this number of items'
    )

    def __init__(self, *args, **kwargs):
        super(ModelList, self).__init__(*args, **kwargs)

    def get_limit(self, value):
        return value.get('limit')

    class Meta:
        icon = 'list-ul'


class FullWidthText(blocks.StreamBlock):
    content = blocks.RichTextBlock(icon='edit')
    media = images_blocks.ImageChooserBlock(icon='image')
    quote = molecules.Quote()
    cta = molecules.CallToAction()
    related_links = molecules.RelatedLinks()
    table = Table(editable=False)
    table_block = AtomicTableBlock(table_options={'renderer':'html'})

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
