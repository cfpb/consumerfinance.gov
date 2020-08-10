from itertools import repeat
from unittest import TestCase

from housing_counselor.cleaner import (
    clean_counselor, clean_counselors, float_or_none, reformat_email,
    reformat_weburl, title_case
)


class TestCleaner(TestCase):
    def mock_counselor(self, **kwargs):
        counselor = {
            'adr1': '123 Main St',
            'adr2': None,
            'agc_ADDR_LATITUDE': '123.45',
            'agc_ADDR_LONGITUDE': '-76.5',
            'city': 'Washington',
            'email': 'hello@domain.com',
            'languages': ['English', 'Spanish'],
            'nme': 'Name',
            'phone1': '202-555-1234',
            'services': ['Foo', 'Bar'],
            'statecd': 'DC',
            'weburl': 'example.com',
            'zipcd': '20001',
        }
        counselor.update(kwargs)
        return counselor

    def test_clean_counselors_empty_list_returns_empty_list(self):
        self.assertEqual(clean_counselors([]), [])

    def test_clean_cleans_list(self):
        counselors = repeat(self.mock_counselor(), 10)
        cleaned = clean_counselors(counselors)
        self.assertEqual(len(cleaned), 10)

    def test_clean_counselor_missing_keys_raises_valueerror(self):
        with self.assertRaises(ValueError):
            clean_counselor({})

    def test_clean_counselor_cleans_valid_data(self):
        counselor = self.mock_counselor(
            agc_ADDR_LATITUDE='-34.56',
            agc_ADDR_LONGITUDE='99.79',
            city='mycity',
            email=' foo@bar.com ',
            extra_key='something',
            nme='MYNAME',
            weburl='foo.com',
        )

        cleaned = clean_counselor(counselor)
        self.assertEqual(cleaned['agc_ADDR_LATITUDE'], -34.56)
        self.assertEqual(cleaned['agc_ADDR_LONGITUDE'], 99.79)
        self.assertEqual(cleaned['city'], 'Mycity')
        self.assertEqual(cleaned['email'], 'foo@bar.com')
        self.assertEqual(cleaned['nme'], 'Myname')
        self.assertEqual(cleaned['weburl'], 'http://foo.com')

    def test_float_or_none_none_returns_none(self):
        self.assertIsNone(float_or_none(None))

    def test_float_or_none_empty_string_returns_none(self):
        self.assertIsNone(float_or_none(''))

    def test_float_or_none_invalid_raises_valueerror(self):
        with self.assertRaises(ValueError):
            float_or_none('foo')

    def test_float_or_none_positive_number(self):
        self.assertEqual(float_or_none('12.34'), 12.34)

    def test_float_or_none_negative_number(self):
        self.assertEqual(float_or_none('-9.8'), -9.8)

    def test_float_or_none_already_float_stays_float(self):
        self.assertEqual(-9.8, -9.8)

    def test_reformat_email_none_returns_none(self):
        self.assertIsNone(reformat_email(None))

    def test_reformat_email_empty_string_returns_none(self):
        self.assertIsNone(reformat_email(''))

    def test_reformat_email_valid_email_returned_properly(self):
        email = 'name@domain.com'
        self.assertEqual(reformat_email(email), email)

    def test_reformat_email_no_dot_returns_none(self):
        self.assertIsNone(reformat_email('foo@bar'))

    def test_reformat_email_no_at_returns_none(self):
        self.assertIsNone(reformat_email('foo.bar'))

    def test_reformat_weburl_none_returns_none(self):
        self.assertIsNone(reformat_weburl(None))

    def test_reformat_weburl_empty_string_returns_none(self):
        self.assertIsNone(reformat_weburl(''))

    def test_reformat_weburl_invalid_returns_none(self):
        self.assertIsNone(reformat_weburl('foo bar'))

    def test_reformat_weburl_notavailable_returns_none(self):
        self.assertIsNone(reformat_weburl('www.notavailable.org'))

    def test_reformat_weburl_adds_http_if_not_present(self):
        self.assertEqual(
            reformat_weburl('www.domain.com'),
            'http://www.domain.com'
        )

    def test_reformat_weburl_keeps_http_if_present(self):
        url = 'http://www.domain.com'
        self.assertEqual(reformat_weburl(url), url)

    def test_reformat_weburl_keeps_https_if_present(self):
        url = 'https://www.domain.com'
        self.assertEqual(reformat_weburl(url), url)

    def test_reformat_weburl_keeps_complex_url(self):
        url = 'https://www.domain.com/path/to/page?query=string&foo=bar'
        self.assertEqual(reformat_weburl(url), url)

    def test_title_case_none_returns_none(self):
        self.assertIsNone(title_case(None))

    def test_title_case_empty_string_returns_none(self):
        self.assertIsNone(title_case(''))

    def test_title_case_multiple_words(self):
        self.assertEqual(
            title_case('SOME WORDS like tHiS'),
            'Some Words Like This'
        )

    def test_title_case_leaves_special_words_lowercase(self):
        self.assertEqual(
            title_case('HELLO FOR THE PEOPLE'),
            'Hello for the People'
        )

    def test_title_case_first_special_word_titlecase(self):
        self.assertEqual(
            title_case('of the people by the people'),
            'Of the People by the People'
        )
