from mock import Mock, patch
from unittest import TestCase

from core.pdf import PDFGenerator


class PDFGeneratorTestCase(TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8000'

    @patch('core.pdf.os.environ.get', return_value='/not/a/real/path')
    def test_imports_from_environment_variable(self, environ_get):
        pdfreactor = PDFGenerator._try_pdfreactor_import()
        environ_get.assert_called_once_with('PDFREACTOR_LIB')

    @patch('core.pdf.os.environ.get', return_value='/not/a/real/path')
    def test_failed_import_returns_null(self, environ_get):
        pdfreactor = PDFGenerator._try_pdfreactor_import()
        self.assertIsNone(pdfreactor)

    @patch('core.pdf.importlib.import_module')
    def test_imports_pdfreactor_class(self, import_module):
        mock_pdfreactor = object()
        import_module.return_value = Mock(PDFreactor=mock_pdfreactor)
        pdfreactor = PDFGenerator._try_pdfreactor_import()
        self.assertEqual(pdfreactor, mock_pdfreactor)

    @patch('core.pdf.importlib.import_module')
    def test_missing_pdfreactor_class_returns_none(self, import_module):
        import_module.return_value = object()
        pdfreactor = PDFGenerator._try_pdfreactor_import()
        self.assertIsNone(pdfreactor)

    def test_pdfreactor_build_calls_constructor(self):
        mock_pdfreactor = Mock()
        pdfreactor_cls = Mock(return_value=mock_pdfreactor)
        pdfreactor = PDFGenerator._build_pdfreactor(
            pdfreactor_cls,
            base_url=self.base_url
        )
        self.assertEqual(pdfreactor, mock_pdfreactor)

    @patch('core.pdf.os.environ.get', return_value='abc123')
    def test_pdfreactor_build_sets_license(self, environ_get):
        mock_pdfreactor = Mock()
        pdfreactor_cls = Mock(return_value=mock_pdfreactor)
        pdfreactor = PDFGenerator._build_pdfreactor(
            pdfreactor_cls,
            base_url=self.base_url
        )
        pdfreactor.setLicenseKey.assert_called_once_with('abc123')

    def test_pdfreactor_build_sets_base_url(self):
        mock_pdfreactor = Mock()
        pdfreactor_cls = Mock(return_value=mock_pdfreactor)
        pdfreactor = PDFGenerator._build_pdfreactor(
            pdfreactor_cls,
            base_url=self.base_url
        )
        pdfreactor.setBaseURL.assert_called_once_with(self.base_url)

    def test_prep_html_converts_to_utf8(self):
        str = u'Citro\xebn'
        prepped = PDFGenerator._prep_html(str)
        self.assertEqual(prepped, 'Citro\xc3\xabn')
        self.assertIsInstance(prepped, basestring)

    def test_prep_html_replaces_left_quote(self):
        str = u'abc\u2018def'
        self.assertEqual(PDFGenerator._prep_html(str), "abc'def")

    def test_prep_html_replaces_right_quote(self):
        str = u'abc\u2019def'
        self.assertEqual(PDFGenerator._prep_html(str), "abc'def")

    @patch('core.pdf.PDFGenerator._try_pdfreactor_import')
    def test_valid_pdfreactor_enabled(self, pdfreactor_import):
        self.assertTrue(PDFGenerator(self.base_url).enabled)

    @patch('core.pdf.PDFGenerator._try_pdfreactor_import', return_value=None)
    def test_invalid_pdfreactor_not_enabled(self, pdfreactor_import):
        self.assertFalse(PDFGenerator(self.base_url).enabled)

    @patch('core.pdf.PDFGenerator._try_build_pdfreactor')
    def test_generate_pdf_calls_pdfreactor(self, try_build_pdfreactor):
        pdfreactor = Mock()
        try_build_pdfreactor.return_value = pdfreactor
        html = '<html><body>hello world</body></html>'
        pdf = PDFGenerator(self.base_url).generate_pdf(html)
        pdfreactor.renderDocumentFromContent.assert_called_once_with(html)

    @patch('core.pdf.PDFGenerator._try_build_pdfreactor')
    def test_generate_pdf_returns_pdfreactor(self, try_build_pdfreactor):
        pdfreactor = Mock()
        try_build_pdfreactor.return_value = pdfreactor
        pdf = PDFGenerator(self.base_url).generate_pdf('abc123')
        self.assertEquals(
            pdfreactor.renderDocumentFromContent.return_value,
            pdf
        )
