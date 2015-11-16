from django.core.exceptions import ValidationError

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from . import atoms


def isRequired(field_name):
    return [str(field_name) + ' is required.']


class HalfWidthLinkBlob(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    content = blocks.RichTextBlock(blank=True)
    links = blocks.ListBlock(blocks.StructBlock([
        ('text', blocks.CharBlock(required=False)),
        ('url', blocks.URLBlock(required=False)),
    ], icon='user', required=False)
    )

    class Meta:
        icon = 'link'
        template = 'v1/demo/molecules/half_width_link_blob.html'


class ImageText5050(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, required=True)
    description = blocks.RichTextBlock(blank=True)
    image = ImageChooserBlock(required=False)
    image_path = blocks.CharBlock(required=False)
    image_alt = blocks.CharBlock(required=False)
    is_widescreen = blocks.BooleanBlock(required=False)
    is_button = blocks.BooleanBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)

    def clean(self, data):
        error_dict = {}
        try:
            block_data = super(ImageText5050, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)
            block_data = data

        if not block_data['image'] and not block_data['image_path'] and not block_data['image_alt']:
            img_err = ['Please upload or enter an image path']
            error_dict.update({'image': img_err, 'image_path': img_err, 'image_alt': isRequired('Image alt')})

        if block_data['image'] and block_data['image_path']:
            img_err = ['Please select one method of image rendering']
            error_dict.update({
                'image': img_err,
                'image_path': img_err})

        if block_data['image_path'] and not block_data['image_alt']:
            error_dict.update({'image_alt': isRequired('Image Alt')})

        if error_dict:
            raise ValidationError("ImageText5050 validation errors", params=error_dict)
        else:
            return block_data

    class Meta:
        icon = 'image'
        template = 'v1/demo/molecules/image_text_5050.html'


class ImageText2575(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(required=True)
    image = ImageChooserBlock(required=False)
    image_path = blocks.CharBlock(required=False)
    image_alt = blocks.CharBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)
    has_rule = blocks.BooleanBlock(required=False)

    def clean(self, data):
        error_dict = {}
        try:
            block_data = super(ImageText2575, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)
            block_data = data

        if not block_data['image'] and not block_data['image_path'] and not block_data['image_alt']:
            img_err = ['Please upload or enter an image path']
            error_dict.update({'image': img_err, 'image_path': img_err, 'image_alt': isRequired('Image alt')})

        if block_data['image'] and block_data['image_path']:
            img_err = ['Please select one method of image rendering']
            error_dict.update({
                'image': img_err,
                'image_path': img_err})

        if block_data['image_path'] and not block_data['image_alt']:
            error_dict.update({'image_alt': isRequired('Image Alt')})

        if error_dict:
            raise ValidationError("ImageText2575 validation errors", params=error_dict)
        else:
            return block_data

    class Meta:
        icon = 'image'
        template = '_includes/molecules/image-text-25-75.html'


class TextIntroduction(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    intro = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)
    has_rule = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'title'
        template = 'v1/demo/molecules/text_introduction.html'


class Hero(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(required=False)

    image = ImageChooserBlock(required=False)
    image_path = blocks.CharBlock(required=False)
    image_alt = blocks.CharBlock(required=False)

    background_color = blocks.CharBlock(max_length=100, required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)
    is_button = blocks.BooleanBlock(required=False)

    def clean(self, data):
        error_dict = {}
        try:
            block_data = super(Hero, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)
            block_data = data

        if not block_data['image'] and not block_data['image_path'] and not block_data['image_alt']:
            img_err = ['Please upload or enter an image path']
            error_dict.update({'image': img_err, 'image_path': img_err, 'image_alt': isRequired('Image alt')})

        if block_data['image'] and block_data['image_path']:
            img_err = ['Please select one method of image rendering']
            error_dict.update({
                'image': img_err,
                'image_path': img_err})

        if block_data['image_path'] and not block_data['image_alt']:
            error_dict.update({'image_alt': isRequired('Image Alt')})

        if error_dict:
            raise ValidationError("Hero validation errors", params=error_dict)
        else:
            return block_data


    class Meta:
        icon = 'image'
        template = '_includes/molecules/hero.html'


class FormFieldWithButton(blocks.StructBlock):
    btn_text = blocks.CharBlock(max_length=100, required=True)

    required = blocks.BooleanBlock(required=False)


    field_id = blocks.CharBlock(max_length=100, required=False)
    field_info = blocks.CharBlock(max_length=100, required=False)
    field_label = blocks.CharBlock(max_length=100, required=True)
    field_name = blocks.CharBlock(max_length=100, required=False)
    field_palceholder = blocks.CharBlock(max_length=100, required=False)


    class Meta:
        icon = 'image'
        template = 'v1/demo/molecules/form-field-with-button.html'

class CallToAction(blocks.StructBlock):
    slug = blocks.CharBlock(required=True)
    paragraph = blocks.RichTextBlock()
    button = atoms.Hyperlink()

    class Meta:
        template = 'v1/wagtail/molecules/call-to-action.html'
        icon = 'grip'
        label = 'Call to Action'


class ContactAddress(blocks.StructBlock):
    label = blocks.CharBlock(max_length=50)
    title = blocks.CharBlock(max_length=100, required=False)
    street = blocks.CharBlock(max_length=100)
    city = blocks.CharBlock(max_length=50)
    state = blocks.CharBlock(max_length=25)
    zip_code = blocks.CharBlock(max_length=15, required=False)

    class Meta:
        template = 'v1/wagtail/molecules/contact-address.html'
        icon = 'mail'
        label = 'Address'


class ContactEmail(blocks.StructBlock):
    emails = blocks.ListBlock(atoms.Hyperlink(label='Email'))

    class Meta:
        icon = 'mail'
        template = 'v1/wagtail/molecules/contact-email.html'
        label = 'Email'


class ContactPhone(blocks.StructBlock):
    fax = blocks.BooleanBlock(default=False, required=False,
                              label='Is this number a fax?')
    phones = blocks.ListBlock(
        blocks.StructBlock([
            ('number', blocks.CharBlock(max_length=15)),
            ('vanity', blocks.CharBlock(max_length=15, required=False)),
            ('tty', blocks.CharBlock(max_length=15, required=False)),
        ]))

    class Meta:
        icon = 'mail'
        template = 'v1/wagtail/molecules/contact-phone.html'
        label = 'Phone'
