# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailadmin.rich_text import HalloPlugin
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.blocks.stream_block import StreamValue

from ask_cfpb.models import Category, SubCategory
from ask_cfpb.models.pages import AnswerPage
from ask_cfpb.scripts import export_ask_data


class SubCategoryModelAdmin(ModelAdmin):
    model = SubCategory
    menu_label = 'Subcategories'
    menu_icon = 'list-ul'
    list_display = (
        'name', 'weight', 'parent'
    )
    search_fields = (
        'name', 'weight')
    list_filter = ('parent',)


class CategoryModelAdmin(ModelAdmin):
    model = Category
    menu_label = 'Categories'
    menu_icon = 'list-ul'
    list_display = (
        'name', 'name_es', 'intro', 'intro_es')


@modeladmin_register
class MyModelAdminGroup(ModelAdminGroup):
    menu_label = 'Ask CFPB'
    menu_icon = 'list-ul'
    items = (
        CategoryModelAdmin,
        SubCategoryModelAdmin)


def export_data(request):
    if request.method == 'POST':
        return export_ask_data.export_questions(http_response=True)
    return render(request, 'admin/export.html')


@hooks.register('register_rich_text_features')
def register_tips_feature(features):
    features.register_editor_plugin(
        'hallo', 'ask-tips',
        HalloPlugin(
            name='answermodule',
            js=['js/ask_cfpb_tips.js'],
        )
    )


@hooks.register('register_rich_text_features')
def register_html_feature(features):
    features.register_editor_plugin(
        'hallo', 'edit-html',
        HalloPlugin(
            name='editHtmlButton',
            js=['js/html_editor.js'],
        )
    )


def editor_css():
    return format_html(
        '<link rel="stylesheet" href="' +
        settings.STATIC_URL +
        'css/question-tips.css">\n')


hooks.register('insert_editor_css', editor_css)


@hooks.register('register_admin_menu_item')
def register_export_menu_item():
    return MenuItem(
        'Export Ask data',
        reverse('export-ask'),
        classnames='icon icon-download',
        order=99999,
    )


@hooks.register('register_admin_urls')
def register_export_url():
    return [url('export-ask', export_data, name='export-ask')]


def get_feedback_stream_value(page):
    """Delivers a basic feedback module with yes/no buttons and comment box"""
    translation_text = {
        'helpful': {'es': '¿Fue útil esta respuesta?',
                    'en': 'Was this page helpful to you?'},
        'button': {'es': 'Enviar',
                   'en': 'Submit'}
    }
    stream_value = [
        {'type': 'feedback',
         'value': {
             'was_it_helpful_text': translation_text['helpful'][page.language],
             'button_text': translation_text['button'][page.language],
             'intro_text': '',
             'question_text': '',
             'radio_intro': '',
             'radio_text': ('This information helps us '
                            'understand your question better.'),
             'radio_question_1': 'How soon do you expect to buy a home?',
             'radio_question_2': 'Do you currently own a home?',
             'contact_advisory': ''}}]
    return stream_value


@hooks.register('after_create_page')
def after_create_page(request, page):
    if isinstance(page, AnswerPage):
        page.content = StreamValue(
            page.content.stream_block,
            get_feedback_stream_value(page),
            is_lazy=True)
        page.save_revision(user=request.user)
