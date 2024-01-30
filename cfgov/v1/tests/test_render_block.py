from django.template import loader
from django.test import SimpleTestCase

from wagtail import blocks


class RenderBlockTests(SimpleTestCase):
    def render_block(self, block_class, text):
        stream_block = blocks.StreamBlock([("myblock", block_class())])
        stream_value = stream_block.to_python(
            [{"type": "myblock", "value": {"text": text}}]
        )

        tmpl = loader.get_template("v1/includes/templates/render_block.html")
        return tmpl.template.module.render(block=stream_value[0], index=0)

    def test_default_unescape(self):
        class MyBlock(blocks.StructBlock):
            text = blocks.CharBlock()

            class Meta:
                template = "v1/includes/atoms/hyperlink.html"

        self.assertIn("<test>", self.render_block(MyBlock, "<test>"))

    def test_unescape_true(self):
        class MyBlock(blocks.StructBlock):
            text = blocks.CharBlock()

            class Meta:
                template = "v1/includes/atoms/hyperlink.html"
                unescape = True

        self.assertIn("<test>", self.render_block(MyBlock, "<test>"))

    def test_unescape_false(self):
        class MyBlock(blocks.StructBlock):
            text = blocks.CharBlock()

            class Meta:
                template = "v1/includes/atoms/hyperlink.html"
                unescape = False

        self.assertIn("&lt;test&gt", self.render_block(MyBlock, "<test>"))
