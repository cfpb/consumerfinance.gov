import importlib
import os
import sys


class PDFGenerator(object):
    """Class that generates a PDF from an HTML document.

    Args:
        base_url: Root URL to use when resolving relative paths
    """
    def __init__(self, base_url):
        self.pdfreactor = self._try_build_pdfreactor(base_url)

    @property
    def enabled(self):
        return self.pdfreactor is not None

    def generate_pdf(self, html):
        content = self._prep_html(html)
        return self.pdfreactor.renderDocumentFromContent(content)

    @classmethod
    def _try_build_pdfreactor(cls, base_url):
        pdfreactor_cls = cls._try_pdfreactor_import()

        if pdfreactor_cls:
            return cls._build_pdfreactor(pdfreactor_cls, base_url=base_url)

    @staticmethod
    def _try_pdfreactor_import():
        try:
            pdfreactor_lib = os.environ.get('PDFREACTOR_LIB')
            sys.path.append(pdfreactor_lib)
            module = importlib.import_module('PDFreactor')
            return getattr(module, 'PDFreactor')
        except (AttributeError, ImportError):
            pass

    @staticmethod
    def _build_pdfreactor(pdfreactor_cls, base_url):
        license = os.environ.get('PDFREACTOR_LICENSE')
        stylesheet_url = '/static/css/pdfreactor-fonts.css'
        author = 'CFPB'

        pdfreactor = pdfreactor_cls()
        pdfreactor.setBaseURL(base_url)
        pdfreactor.setLogLevel(pdfreactor_cls.LOG_LEVEL_WARN)
        pdfreactor.setLicenseKey(str(license))
        pdfreactor.setAuthor(author)
        pdfreactor.setAddTags(True)
        pdfreactor.setAddBookmarks(True)
        pdfreactor.addUserStyleSheet('', '', '', stylesheet_url)

        return pdfreactor

    @staticmethod
    def _prep_html(html):
        html = html.replace(u'\u2018', "'") # replace left quote character
        html = html.replace(u'\u2019', "'") # replace right quote character
        html = html.encode('utf-8)')

        return html
