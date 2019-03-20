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
from wagtail.wagtailcore.models import Page

from ask_cfpb.models import Answer, AnswerPage, Category, SubCategory
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


@hooks.register('after_create_page')
def create_answer_id(request, page):
    """
    Create an incremented Answer ID for a new AnswerPage and attach it.

    Also create a sister-language page to keep languages in sync.
    """
    if isinstance(page, AnswerPage) and page.answer_base is None:
        new_answer_base = Answer(
            last_user=request.user,
            question=page.title)
        new_answer_base.save()
        new_id = new_answer_base.pk
        if page.get_parent().slug == 'obtener-respuestas':
            page.language = 'es'
            sister_page = AnswerPage(
                live=False,
                language='en',
                title="English draft of {}-en-{}".format(page.title, new_id),
                answer_base=new_answer_base)
            Page.objects.get(slug='ask-cfpb').specific.add_child(
                instance=sister_page)
        else:
            sister_page = AnswerPage(
                live=False,
                language='es',
                title="Spanish draft of {}-es-{}".format(page.title, new_id),
                answer_base=new_answer_base)
            Page.objects.get(slug='obtener-respuestas').specific.add_child(
                instance=sister_page)
        sister_page.save()
        sister_page.save_revision(user=request.user)
        page.answer_base = new_answer_base
        page.title = "{}-{}-{}".format(
            page.title, page.language, new_id)
        page.slug = "{}-{}-{}".format(
            page.slug, page.language, new_id)
        page.save()
        page.save_revision(user=request.user)
