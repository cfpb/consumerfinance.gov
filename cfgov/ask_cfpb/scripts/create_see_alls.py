# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth.models import User
from django.utils.text import slugify

from ask_cfpb.models import AnswerLandingPage, PortalSearchPage
from v1.models import LandingPage, SublandingPage


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
                    'overview': 'A la hora de elegir y utilizar sus cuentas en un banco o cooperativa de crédito, es importante que conozca sus opciones.',  # noqa
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
                    'overview': 'Sus informes y puntajes de crédito tienen un gran impacto sobre sus oportunidades financieras. Nuestros recursos pueden ayudarle a aprender a corregir los errores y a mejorar su historial de crédito a lo largo del tiempo.',  # noqa
                    "portal_topic_id": 4}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Cobro de deudas',
                'child': {
                    'title': 'Cobro de deudas respuestas',
                    'overview': 'Los problemas de cobro de deudas pueden ser un reto. Usted no tiene que enfrentarlse a ellos solo. Nuestros recursos pueden ayudarle a entender cómo funciona el cobro de deudas y cuáles son sus derechos.',  # noqa
                    "portal_topic_id": 5}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Fraudes y estafas',
                'child': {
                    'title': 'Fraudes y estafas respuestas',
                    'overview': 'Perder dinero o propiedad a causa de estafas y fraudes puede ser devastador. Nuestros recursos pueden ayudarle a reconocer, evitar e informar sobre estafas y fraudes.',  # noqa
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
                    'overview': 'Ya sea que usted esté pensando en comprar una vivienda, tenga un préstamo hipotecario, o problemas para pagar su hipoteca, tenemos los recursos para ayudarle en todo momento.',  # noqa
                    "portal_topic_id": 9}},
            {
                'model': SublandingPage,
                    'pk': None,
                'title': 'Tarjetas prepagadas',
                'child': {
                    'title': 'Tarjetas prepagadas respuestas',
                    'overview': 'Si está pensando en obtener una cuenta o tarjeta prepagada, tenemos información que le puede ayudar a elegir la más adecuada para usted. También podemos ayudarle a entender sus derechos.',  # noqa
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
                    'overview': 'Ya sea que se esté preparando para la universidad, para asistir a un centro de enseñanza o si ya está pagando sus préstamos estudiantiles, nosotros tenemos las.',  # noqa
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
                    "overview": "When you’re shopping for a new auto loan, it’s important to know the right questions to ask. Preparing can help you save money, reduce stress, and get the auto loan that’s right for you.",  # noqa
                    "portal_topic_id": 1}},
            {
                'model': SublandingPage,
                'pk': 12297,
                "title": "Bank accounts and services",
                'child': {
                    'title': 'Bank account answers',
                    "overview": "When choosing and using your bank or credit union account, it’s important to know your options.",  # noqa
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
                    "overview": "Your credit reports and scores have a major impact on your financial opportunities. Our resources can help you learn how to correct inaccuracies and improve your credit record.",  # noqa
                    "portal_topic_id": 4}},
            {
                'model': SublandingPage,
                'pk': 12238,
                "title": "Debt Collection",
                'child': {
                    'title': 'Debt collection answers',
                    "overview": "Debt collection issues can be challenging. You don't have to face them alone. Our resources can help you understand how debt collection works and what your rights are.",  # noqa
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
                'model': SublandingPage,
                'pk': None,
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
                    "overview": "Whether you’re thinking of buying a home, already have a home loan, or are having trouble paying your mortgage, we have resources to help you every step of the way.",  # noqa
                    "portal_topic_id": 9}},
            {
                'model': SublandingPage,
                'pk': 12599,
                'title': 'Prepaid cards',
                'child': {
                    'title': 'Prepaid card answers',
                    "overview": "If you’re considering getting a prepaid card or account, we have information that can help you choose the right one for you and better understand your rights.",  # noqa
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
                    "overview": "Whether you are preparing for college, attending school, or already repaying your student loans, we have tools and resources to help you make the best decisions for you.",  # noqa
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
