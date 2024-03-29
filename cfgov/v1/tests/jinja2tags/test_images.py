from django.test import TestCase

from model_bakery import baker

from v1.atomic_elements.atoms import ImageBasic
from v1.jinja2tags.images import image_alt_value
from v1.models import CFGOVImage, CFGOVRendition


class TestImageAltValue(TestCase):
    def test_no_rendition_or_block_passed(self):
        self.assertEqual(image_alt_value(None), "")

    def test_rendition_no_alt_text_set(self):
        rendition = CFGOVRendition(image=CFGOVImage())
        self.assertEqual(image_alt_value(rendition), "")

    def test_rendition_with_alt_text(self):
        rendition = CFGOVRendition(image=CFGOVImage(alt="Alt text"))
        self.assertEqual(image_alt_value(rendition), "Alt text")

    def test_block_no_image_in_block(self):
        block = ImageBasic()
        value = block.to_python({})
        self.assertEqual(image_alt_value(value), "")

    def test_block_no_alt_text_set(self):
        image_no_alt_text = baker.make(CFGOVImage, alt="")
        block = ImageBasic()
        value = block.to_python({"upload": image_no_alt_text.pk, "alt": ""})
        self.assertEqual(image_alt_value(value), "")

    def test_block_alt_text_on_upload(self):
        image_with_alt_text = baker.make(CFGOVImage, alt="Alt text on upload")
        block = ImageBasic()
        value = block.to_python({"upload": image_with_alt_text.pk, "alt": ""})
        self.assertEqual(image_alt_value(value), "Alt text on upload")

    def test_block_alt_text_on_block(self):
        image_no_alt_text = baker.make(CFGOVImage, alt="")
        block = ImageBasic()
        value = block.to_python(
            {"upload": image_no_alt_text.pk, "alt": "Alt text on block"}
        )
        self.assertEqual(image_alt_value(value), "Alt text on block")

    def test_block_alt_text_on_both(self):
        image_with_alt_text = baker.make(CFGOVImage, alt="Alt text on upload")
        block = ImageBasic()
        value = block.to_python(
            {"upload": image_with_alt_text.pk, "alt": "Alt text on block"}
        )
        self.assertEqual(image_alt_value(value), "Alt text on block")

    def test_dict(self):
        self.assertEqual(
            image_alt_value({"foo": "bar", "alt": "Alt text in dict"}),
            "Alt text in dict",
        )

    def test_dict_no_value(self):
        self.assertEqual(image_alt_value({"foo": "bar"}), "")
