from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail.core import blocks
from wagtail.images import blocks as images_blocks


class ImageMapCoordinates(blocks.StructBlock):
    left = blocks.FloatBlock(required=True, min_value=0, max_value=100)
    top = blocks.FloatBlock(required=True, min_value=0, max_value=100)
    width = blocks.FloatBlock(required=True, min_value=0, max_value=100)
    height = blocks.FloatBlock(required=True, min_value=0, max_value=100)

    def clean(self, value):
        cleaned = super(ImageMapCoordinates, self).clean(value)
        errors = {}
        if cleaned.get('left') + cleaned.get('width') > 100:
            errors['left'] = errors['width'] = ErrorList([
                'Sum of left and width values should not exceed 100.'
            ])
        if cleaned.get('top') + cleaned.get('height') > 100:
            errors['top'] = errors['height'] = ErrorList([
                'Sum of top and height values should not exceed 100.'
            ])
        if errors:
            raise ValidationError(
                'Validation error in ImageMapCoordinates',
                params=errors
            )
        return cleaned


class ExplainerNote(blocks.StructBlock):
    coordinates = ImageMapCoordinates(
        form_classname='coordinates',
        label='Note image map coordinates',
        help_text='Enter percentage values to define the area '
                  'that will be highlighted on the image for this note.')
    heading = blocks.CharBlock(required=True, label='Note heading')
    body = blocks.RichTextBlock(
        required=True,
        features=[
            'bold', 'italic', 'link', 'document-link'
        ],
        label='Note text')


class ExplainerCategory(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        label='Category title',
        help_text='Optional. Leave blank if there is only '
                  'one type of note for this image.'
    )
    notes = blocks.ListBlock(
        ExplainerNote(
            form_classname='explainer_notes',
            required=False
        ),
        default=[],
    )


class ExplainerPage(blocks.StructBlock):
    image = images_blocks.ImageChooserBlock(required=True, icon='image')
    categories = blocks.ListBlock(ExplainerCategory(required=False))


class Explainer(blocks.StructBlock):
    pages = blocks.ListBlock(ExplainerPage(required=False))

    class Meta:
        template = 'form-explainer/blocks/explainer.html'
        icon = 'doc-full-inverse'
        label = 'Explainer'

    class Media:
        js = ['form-explainer/form-explainer.js']
