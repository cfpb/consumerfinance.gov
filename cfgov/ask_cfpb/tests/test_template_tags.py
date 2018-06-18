from __future__ import unicode_literals

from unittest import TestCase

from ask_cfpb.templatetags.accent_stripper import strip_accents


class StripAccentTests(TestCase):

    def test_strip_unicode(self):
        code_point_map = [
            ('\N{LATIN SMALL LETTER N WITH TILDE}', 'n'),
            ('\N{LATIN CAPITAL LETTER N WITH TILDE}', 'N'),
            ('\N{LATIN CAPITAL LETTER O WITH ACUTE}', 'O'),
            ('\N{LATIN SMALL LETTER A WITH ACUTE}', 'a'),
            ('\N{LATIN SMALL LETTER E WITH ACUTE}', 'e'),
            ('\N{LATIN SMALL LETTER I WITH ACUTE}', 'i'),
            ('\N{INVERTED QUESTION MARK}', ''),
        ]
        for code in code_point_map:
            self.assertEqual(
                strip_accents(code[0]), code[1]
            )
