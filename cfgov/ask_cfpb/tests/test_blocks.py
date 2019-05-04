from __future__ import unicode_literals
from django.test import TestCase

from ask_cfpb.models.blocks import Tip, AskAnswerContent


class TipTestCase(TestCase):
	def test_tip_html(self):
		block = Tip()
		value = {
			'content': 'Test tip'
		}
		html = block.render(value)
		self.assertIn('<aside class="m-inset', html)
		self.assertIn('<h4>Tip</h4>', html)
		self.assertIn('<div class="rich-text">Test tip</div>', html)
		self.assertIn('</aside>', html)

class ContentBlockTestCase(TestCase):
	def test_inset_wrapper_with_tip(self):
		tip = {
			'type': 'tip',
			'value': {
				'content': 'Content'
			}
		}
		block = AskAnswerContent()
		value = block.to_python([tip])
		html = block.render(value)
		self.assertIn('<div class="inset-row">', html)
		self.assertIn('<aside class="m-inset', html)
		self.assertIn('<h4>Tip</h4>', html)
		self.assertIn('<div class="rich-text">Content</div>', html)
		self.assertIn('</aside></div>', html)

	def test_inset_wrapper_with_tip_and_text(self):
		tip = {
			'type': 'tip',
			'value': {
				'content': 'Tip content'
			}
		}
		text = {
			'type': 'text',
			'value': {
				'content': 'text'
			}
		}
		block = AskAnswerContent()
		value = block.to_python([tip, text])
		html = block.render(value)
		self.assertIn('<div class="inset-row">', html)
		self.assertIn('<aside class="m-inset', html)
		self.assertIn('<h4>Tip</h4>', html)
		self.assertIn('<div class="rich-text">Tip content</div>', html)
		self.assertIn('</aside>', html)
		self.assertIn('<div class="rich-text">text</div></div>', html)
