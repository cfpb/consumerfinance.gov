import re

from functools import partial

from markdown import markdown, util
from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension


# If we're on Python 3.6+ we have SHA3 built-in, otherwise use the back-ported
# sha3 library.
try:
    from hashlib import sha3_224
except ImportError:
    from sha3 import sha3_224


class RegulationsExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.parser.blockprocessors.add('labeledparagraph',
                                      LabeledParagraphProcessor(md.parser),
                                      '_begin')


class LabeledParagraphProcessor(ParagraphProcessor):
    """ Process paragraph blocks, including those with labels.
    This processor entirely replaces the standard ParagraphProcessor in
    order to ensure that all paragraphs are labeled in some way. """

    RE = re.compile(r'(?:^|\n){([\w\-]+)}(?:\s?)(.*)(?:\n|$)')

    def test(self, parent, block):
        # return self.RE.search(block)
        return True

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.RE.search(block)

        if match:
            # If there's a match, then this is a labeled paragraph. We'll add
            # the paragraph tag, label id, and initial text, then process the
            # rest of the blocks normally.
            label, text = match.group(1), match.group(2)
            p = util.etree.SubElement(parent, 'p')
            p.set('id', label)
            p.text = text.lstrip()

        elif block.strip():
            if self.parser.state.isstate('list'):
                # Pass off to the ParagraphProcessor for lists
                super(ParagraphProcessor, self).run(parent, blocks)
            else:
                # Generate a label that is a hash of the block contents. This
                # way it won't change unless the rest of this block changes.
                text = block.lstrip()
                label = sha3_224(text.encode('utf-8')).hexdigest()
                p = util.etree.SubElement(parent, 'p')
                p.set('id', label)
                p.text = text


def makeExtension(*args, **kwargs):
    return RegulationsExtension(*args, **kwargs)


# Create a regdown() convenience function that takes text and parses it with
# the RegulationsExtension configured it as an extension
regdown = partial(
    markdown,
    extensions=[RegulationsExtension()]
)
