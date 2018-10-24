# -*- coding: utf-8 -*-
"""
# Regdown

Regdown is an extension for Markdown that supports features to make federal
regulations easier to navigate and read.

These features include:

- Labeled paragraphs
- Block references
- Inline pseudo forms

## Labeled Paragraphs

`{label} Paragraph text`

Each paragraph can have a defined label, using `{label}` syntax at the start of
the paragraph. This is translated into an `id` attribute on the resulting HTML
paragraph element. If no label is given, the contents of the paragraph are
hashed to generate a unique `id` for that paragraph. This makes any paragraph
in the text directly linkable.

## Block references

`see(label)`

References can be placed before or after paragraphs to labeled paragraphs in
other Markdown documents. When a `contents_resolver` callback and
`url_resolver` callback are provided, the text of those other paragraphs can
be looked up and inserted into the document making the reference. If
`render_block_reference` callback is provided, custom rendering of the
referenced text to HTML can be performed.

Callbacks:

- `contents_resolver(label)`: resolve the paragraph label and return the
  Markdown contents of that paragraph if the paragraph exists.
- `url_resolver(label)`: resolve the paragraph label and return a URL to that
  paragraph if the paragraph exists.
- `render_block_reference(contents, url=None)`: render the contents of a block
  reference to HTML. The url to the reference may be give as a keyword argument
  if `url_resolver` is provided.

## Pseudo Forms

`Form field: __`
`__Form Field`
`inline__fields__

Example print forms, where the `__` indicate a space for hand-written input.
Can be any number of underscores between 2 and 50.

## Section symbols

`§ 1024.5(d)`
`§1024.5(d)`

Section symbols will always have a non-breaking space (&nbsp;) inserted between
them and whatever follows to avoid hanging a symbol at the end of a line.
"""
from __future__ import unicode_literals

import re

from markdown import markdown, util
from markdown.blockprocessors import BlockProcessor, ParagraphProcessor
from markdown.extensions import Extension
from markdown.inlinepatterns import DoubleTagPattern, Pattern, SimpleTagPattern
from mdx_emdash import EmDashExtension


# If we're on Python 3.6+ we have SHA3 built-in, otherwise use the back-ported
# sha3 library.
try:
    from hashlib import sha3_224
except ImportError:  # pragma: no cover
    from sha3 import sha3_224


# **strong**
STRONG_RE = r'(\*{2})(.+?)\2'

# ***strongem*** or ***em*strong**
EM_STRONG_RE = r'(\*)\2{2}(.+?)\2(.*?)\2{2}'

# ***strong**em*
STRONG_EM_RE = r'(\*)\2{2}(.+?)\2{2}(.*?)\2'

# Form field: __
# __Form Field
# inline__fields__
PSEUDO_FORM_RE = r'(?P<underscores>_{2,50})(?P<line_ending>\s*$)?'

# Section symbol §
SECTION_SYMBOL_RE = r'(?P<section_symbol>§)\s+'


DEFAULT_URL_RESOLVER = lambda l: ''
DEFAULT_CONTENTS_RESOLVER = lambda l: ''
DEFAULT_RENDER_BLOCK_REFERENCE = lambda c, **kwargs: \
    '<blockquote>{}</blockquote>'.format(regdown(c))


class RegulationsExtension(Extension):

    config = {
        'url_resolver': [
            DEFAULT_URL_RESOLVER,
            'Function to resolve the URL of a reference. '
            'Should return (title, url).'
        ],
        'contents_resolver': [
            DEFAULT_CONTENTS_RESOLVER,
            'Function to resolve the contents of a reference. '
            'Should return markdown contents of the reference or an empty '
            'string.'
        ],
        'render_block_reference': [
            DEFAULT_RENDER_BLOCK_REFERENCE,
            'Function that will render a block reference'
        ],
    }

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        # Add inline pseudo form pattern. Replace all inlinePatterns that
        # include an underscore with patterns that do not include underscores.
        md.inlinePatterns['em_strong'] = DoubleTagPattern(
            EM_STRONG_RE, 'strong,em'
        )
        md.inlinePatterns['strong_em'] = DoubleTagPattern(
            STRONG_EM_RE, 'em,strong'
        )
        md.inlinePatterns['strong'] = SimpleTagPattern(
            STRONG_RE, 'strong'
        )
        md.inlinePatterns['pseudo-form'] = PseudoFormPattern(
            PSEUDO_FORM_RE
        )
        md.inlinePatterns['section-symbol'] = SectionSymbolPattern(
            SECTION_SYMBOL_RE
        )
        del md.inlinePatterns['emphasis2']

        # Add block reference processor for `see(label)` syntax
        md.parser.blockprocessors.add(
            'blockreference',
            BlockReferenceProcessor(
                md.parser,
                url_resolver=self.getConfig('url_resolver'),
                contents_resolver=self.getConfig('contents_resolver'),
                render_block_reference=self.getConfig(
                    'render_block_reference'),
            ),
            '<paragraph'
        )

        # Replace the default paragraph processor with one that handles
        # `{label}` syntax and gives default hash-based ids to paragraphs
        md.parser.blockprocessors['paragraph'] = \
            LabeledParagraphProcessor(md.parser)

        # Delete the ordered list processor
        del md.parser.blockprocessors['olist']


class PseudoFormPattern(Pattern):
    """ Return a <span class="pseudo-form"></span> element for matches of the
    given pseudo-form pattern. """

    def handleMatch(self, m):
        el = util.etree.Element('span')
        el.set('class', 'regdown-form')
        if m.group('line_ending') is not None:
            el.set('class', 'regdown-form_extend')
            util.etree.SubElement(el, 'span')
        el.text = m.group('underscores')
        return el


class SectionSymbolPattern(Pattern):
    """ Make whitespace after a section symbol non-breaking """

    def handleMatch(self, m):
        return '{section}{stx}{char}{etx}#160;'.format(
            section=m.group('section_symbol'),
            stx=util.STX,
            char=ord('&'),
            etx=util.ETX
        )


class LabeledParagraphProcessor(ParagraphProcessor):
    """ Process paragraph blocks, including those with labels.
    This processor entirely replaces the standard ParagraphProcessor in
    order to ensure that all paragraphs are labeled in some way. """

    RE = re.compile(r'(?:^){(?P<label>[\w\-]+)}(?:\s?)(?P<text>.*)(?:\n|$)')

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
            label, text = match.group('label'), match.group('text')
            # Labeled paragraphs without text should use a div element
            if text == '':
                el = util.etree.SubElement(parent, 'div')
            else:
                el = util.etree.SubElement(parent, 'p')
            el.set('id', label)

            # We use CSS classes to indent paragraph text. To get the correct
            # class, we count the number of dashes in the label to determine
            # how deeply nested the paragraph is. Inline interps have special
            # prefixes that are removed before counting the dashes.
            # e.g. 6-a-Interp-1 becomes 1 and gets a `level-0` class
            # e.g. 12-b-Interp-2-i becomes 2-i and gets a `level-1` class
            label = re.sub(
                r'^(\w+\-)+interp\-', '', label, flags=re.IGNORECASE
            )

            # Appendices also have special prefixes that need to be stripped.
            # e.g. A-1-a becomes a and gets a `level-0` class
            # e.g. A-2-d-1 becomes d-1 and gets a `level-1` class
            label = re.sub(r'^[A-Z]\d?\-\w+\-?', '', label)
            level = label.count('-')
            class_name = 'regdown-block level-{}'.format(level)
            el.set('class', class_name)

            el.text = text.lstrip()

        elif block.strip():
            if self.parser.state.isstate('list'):
                # Pass off to the ParagraphProcessor for lists
                super(ParagraphProcessor, self).run(
                    parent, blocks
                )  # pragma: no cover
            else:
                # Generate a label that is a hash of the block contents. This
                # way it won't change unless the rest of this block changes.
                text = block.lstrip()
                label = sha3_224(text.encode('utf-8')).hexdigest()
                class_name = 'regdown-block'
                p = util.etree.SubElement(parent, 'p')
                p.set('id', label)
                p.set('class', class_name)

                p.text = text


class BlockReferenceProcessor(BlockProcessor):
    """ Process `see(label)` as an blockquoted reference.
    To render the block reference, the extension must be initialized with a
    callable render_block_reference option that will take the contents of
    the block reference, rendering to HTML, and return the HTML.
    """

    RE = re.compile(r'(?:^)see\((?P<label>[\w-]+)\)(?:\n|$)')

    def __init__(self,
                 parser,
                 url_resolver=None,
                 contents_resolver=None,
                 render_block_reference=None):
        super(BlockReferenceProcessor, self).__init__(parser)
        self.url_resolver = url_resolver
        self.contents_resolver = contents_resolver
        self.render_block_reference = render_block_reference

    def test(self, parent, block):
        return self.RE.search(block)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.RE.match(block)

        if match:
            # Without a contents_resolver, we can't resolve block contents
            if (not callable(self.contents_resolver) or
                    not callable(self.render_block_reference)):
                return

            label = match.group('label')
            contents = self.contents_resolver(label)
            url = self.url_resolver(label)

            if contents == '':
                return

            rendered_contents = self.render_block_reference(
                contents,
                url=url
            )

            parent.append(
                util.etree.fromstring(rendered_contents.encode('utf-8'))
            )


def makeExtension(*args, **kwargs):
    return RegulationsExtension(*args, **kwargs)


def regdown(text, **kwargs):
    """ Regdown convenience function
    Takes text and parses it with the RegulationsExtention configured with
    the given keyword arguments. """
    return markdown(
        text,
        extensions=[
            'markdown.extensions.tables',
            RegulationsExtension(**kwargs),
            EmDashExtension(),
        ],
        **kwargs
    )


def extract_labeled_paragraph(label, text, exact=True):
    """ Extract all the Regdown between the given label and the next.
    This utility function extracts all text between a labeled paragraph
    (with leading {label}) and the next labeled paragraph. If exact is False,
    it will match all paragraphs with labels that *begin with* the given
    label.  """
    para_lines = []

    for line in text.splitlines(True):
        match = LabeledParagraphProcessor.RE.search(line)
        if match:
            # It's the correct label and we want an exact match
            if exact and match.group('label') == label:
                para_lines.append(line)

            # We don't want an exact match and the label starts with our given
            # label
            elif not exact and match.group('label').startswith(label):
                para_lines.append(line)

            # We've already found a label, and this is another one
            elif len(para_lines) > 0:
                break

        # We've found a label and haven't found the next
        elif len(para_lines) > 0:
            para_lines.append(line)

    return ''.join(para_lines)
