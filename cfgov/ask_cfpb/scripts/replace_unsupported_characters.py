import os

from django.contrib.auth.models import User

from ask_cfpb.models.answer_page import AnswerPage


# A dictionary for swapping misencodings with valid unicode code points
unicode_swaps = {
    "\x91": "\u2018",  # Left Single Quotation Mark
    "\x92": "\u2019",  # Right Single Quotation Mark
    "\x93": "\u201C",  # Left Double Quotation Mark
    "\x94": "\u201D",  # Right Double Quotation Mark
    "\x95": "\u2022",  # Bullet
    "\x96": "\u2013",  # En Dash
    "\x97": "\u2014",  # Em Dash
    "\x98": "\u02DC",  # Small Tilde
    "\x99": "\u2122",  # Trade Mark Sign
    "\xac": "-",  # Not Sign (a dash with a hook on end)
    "\u200b": "",  # Zero Width Space (We neve want this)
    "\u25e6": "- ",  # White Bullet
    "\u25cb": "- ",  # White Circle
    "\uf0a7": " ",  # misencoding (no such code point)
}


def fix(text, string):
    return text.replace(string, unicode_swaps[string])


def run():
    migration_user_pk = os.getenv("MIGRATION_USER_PK", 9999)
    user = User.objects.filter(id=migration_user_pk).first()
    for page in AnswerPage.objects.filter(live=True):
        fixed = False
        for string in unicode_swaps:
            if string in page.question:
                page.question = fix(page.question, string)
                fixed = True
            if string in page.answer:
                page.answer = fix(page.answer, string)
                fixed = True
            if string in page.snippet:
                page.snippet = fix(page.snippet, string)
                fixed = True
        if fixed:
            page.save_revision(user=user).publish()
