# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth.models import User
from django.utils.text import slugify

from ask_cfpb.models import AnswerLandingPage, PortalSearchPage
from v1.models import BrowsePage, LandingPage, SublandingPage


PARENT_PAGE_MAP = {
    'es': {
        # Obtener respuestas
        'grandparent': AnswerLandingPage.objects.get(pk=5704),
        'parents': [
            {
                'model': SublandingPage,
                'pk': None,
                'title': 'Préstamos para vehículos',
                'child': {
                    'title': 'Préstamos para vehículos respuestas',
                    'overview': '',
                    "portal_topic_id": 1}},
            {
                'model': SublandingPage,
                'pk': None,
                'title': 'Cuentas bancarias',
                'child': {
                    'title': 'Cuentas bancaria respuestas',
                    'overview': '',
                    "portal_topic_id": 2}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Tarjetas de crédito',
                'child': {
                    'title': 'Tarjetas de crédito respuestas',
                    'overview': '',
                    "portal_topic_id": 3}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Informes y puntajes de crédito',
                'child': {
                    'title': 'Informes y puntajes de crédito respuestas',
                    'overview': '',
                    "portal_topic_id": 4}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Cobro de deudas',
                'child': {
                    'title': 'Cobro de deudas respuestas',
                    'overview': '',
                    "portal_topic_id": 5}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Fraudes y estafas',
                'child': {
                    'title': 'Fraudes y estafas respuestas',
                    'overview': '',
                    "portal_topic_id": 7}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Transferencias de dinero',
                'child': {
                    'title': 'Transferencias de dinero respuestas',
                    'overview': '',
                    "portal_topic_id": 8}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Hipotecas',
                'child': {
                    'title': 'Hipotecas respuestas',
                    'overview': '',
                    "portal_topic_id": 9}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Tarjetas prepagadas',
                'child': {
                    'title': 'Tarjetas prepagadas respuestas',
                    'overview': '',
                    "portal_topic_id": 11}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Hipotecas inversas',
                'child': {
                    'title': 'Hipotecas inversas respuestas',
                    'overview': '',
                    "portal_topic_id": 12}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Préstamos estudiantiles',
                'child': {
                    'title': 'Préstamos estudiantiles respuestas',
                    'overview': '',
                    "portal_topic_id": 13}},
        ]
    },
    'en': {
        # Consumer tools
        'grandparent': LandingPage.objects.get(pk=12051),
        'parents': [
            {
                'model': SublandingPage,
                'pk': 12309,
                "title": "Auto loans",
                'child': {
                    'title': 'Auto loan answers',
                    "overview": "When you\u2019re shopping for a new auto loan, know the right questions to ask. Get answers to frequently asked auto loan questions.",  # noqa
                    "portal_topic_id": 1}},
            {
                'model': SublandingPage,
                'pk': 12297,
                "title": "Bank accounts and services",
                'child': {
                    'title': 'Bank account answers',
                    "overview": "Do you know how to avoid overdraft fees and find out what to do if someone took money from your bank account without permission? Learn more about these and other issues.",  # noqa
                    "portal_topic_id": 2}},
            {
                'model': SublandingPage,
                'pk': None,
                "title": "Credit cards",
                'child': {
                    'title': 'Credit card answers',
                    "overview": "Whether you’re shopping for a new card or managing an existing card, it helps to have the facts. From late fees to lost cards, get answers to your credit card questions.",  # noqa
                    "portal_topic_id": 3}},
            {
                'model': SublandingPage,
                'pk': 12201,
                "title": "Credit reports and scores",
                'child': {
                    'title': 'Credit report answers',
                    "overview": "You can take action to get your credit report and to get and keep a good credit score. Find out how with our frequently asked questions.",  # noqa
                    "portal_topic_id": 4}},
            {
                'model': SublandingPage,
                'pk': 12238,
                "title": "Debt Collection",
                'child': {
                    'title': 'Debt collection answers',
                    "overview": "Did you know that debt collectors generally can’t call you after 9 p.m.? Learn about debt collection, harassment, and more by searching or browsing.",  # noqa
                    "portal_topic_id": 5}},
            {
                'model': SublandingPage,
                'pk': 12283,
                'title': 'Fraud and scams',
                'child': {
                    'title': 'Fraud and scam answers',
                    "overview": "Losing money or property to scams and fraud can be devastating. Our resources can help you prevent, recognize, and report scams and fraud.",  # noqa
                    "portal_topic_id": 7}},
            {
                'model': BrowsePage,
                'pk': 12299,
                'title': 'Money transfers',
                'child': {
                    'title': 'Money transfer answers',
                    "overview": "What are money and remittance transfers? And how do they work? Learn more about transferring money from the United States to other countries and your consumer protections.",  # noqa
                    "portal_topic_id": 8}},
            {
                'model': SublandingPage,
                'pk': 12279,
                'title': 'Mortgages',
                'child': {
                    'title': 'Mortgage answers',
                    "overview": "Whether you are getting a mortgage, having trouble paying your mortgage, or want to learn about reverse mortgages, we have answers to your questions.",  # noqa
                    "portal_topic_id": 9}},
            {
                'model': SublandingPage,
                'pk': 12599,
                'title': 'Prepaid cards',
                'child': {
                    'title': 'Prepaid card answers',
                    "overview": "Prepaid cards might look like debit and credit cards, but there are some important differences between them. Learn about fees and charges, and find answers to common questions.",  # noqa
                    "portal_topic_id": 11}},
            {
                'model': SublandingPage,
                'pk': None,
                'title': 'Reverse mortgages',
                'child': {
                    'title': 'Reverse mortgage answers',
                    "overview": "",  # noqa
                    "portal_topic_id": 12}},
            {
                'model': SublandingPage,
                'pk': 12290,
                'title': 'Student loans',
                'child': {
                    'title': 'Student loan answers',
                    "overview": "Student loans are complicated. We have answers to questions about how to pay off your loans and the repayment programs available to you.",  # noqa
                    "portal_topic_id": 13}},
        ]
    },
}


def create_see_all_pages(language):
    """Create PortalSearchPages for a given language."""
    answer_slugs = {
        'es': 'respuestas',
        'en': 'answers'
    }
    migration_user_pk = os.getenv('MIGRATION_USER_PK', 9999)
    user = User.objects.filter(id=migration_user_pk).first()
    page_map = PARENT_PAGE_MAP.get(language)
    grandparent = page_map.get('grandparent')
    # get or create parent pages and create child topic pages
    for parent_map in page_map.get('parents'):
        child_map = parent_map.get('child')
        title = parent_map.get('title')
        print("Creating parent and child pages for {}".format(title).encode(
            'utf-8'))
        if parent_map['pk']:
            parent_page = parent_map['model'].objects.get(
                pk=parent_map['pk'])
        else:
            parent_page = parent_map['model'](
                title=title,
                language=language,
                slug=slugify(title))
            grandparent.add_child(instance=parent_page)
            parent_page.save()
            parent_page.save_revision(user=user).publish()
            parent_page.unpublish()
        child_page = PortalSearchPage(
            title=child_map.get('title'),
            language=language,
            slug=answer_slugs.get(language),
            overview=child_map.get('overview'))
        parent_page.add_child(instance=child_page)
        child_page.save()
        child_page.portal_topic_id = child_map.get('portal_topic_id')
        child_page.save_revision(user=user).publish()


def run(*args):
    if args and args[0] == 'es':
        create_see_all_pages('es')
    elif args and args[0] == 'en':
        create_see_all_pages('en')
    else:
        print(
            "Please provide a language value. Example:\n"
            "./cfgov/manage.py runscript create_see_alls --script-args 'en'")
