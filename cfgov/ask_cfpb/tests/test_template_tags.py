from unittest import TestCase

from ask_cfpb.templatetags.accent_stripper import strip_accents


class StripAccentTests(TestCase):

    def test_strip_unicode(self):
        code_point_map = [
            ('\N{LATIN SMALL LETTER N WITH TILDE}', b'n'),
            ('\N{LATIN CAPITAL LETTER N WITH TILDE}', b'N'),
            ('\N{LATIN CAPITAL LETTER O WITH ACUTE}', b'O'),
            ('\N{LATIN SMALL LETTER A WITH ACUTE}', b'a'),
            ('\N{LATIN SMALL LETTER E WITH ACUTE}', b'e'),
            ('\N{LATIN SMALL LETTER I WITH ACUTE}', b'i'),
            ('\N{INVERTED QUESTION MARK}', b''),
        ]
        for code in code_point_map:
            self.assertEqual(
                strip_accents(code[0]), code[1]
            )
