from .base import CFGOVPage


class HomePage(CFGOVPage):
    parent_page_types = ['wagtailcore.Page']  # Sets page to only be createable at the root
