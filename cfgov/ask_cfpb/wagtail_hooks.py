from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.html import format_html

try:
    from wagtail.admin.menu import MenuItem
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin.menu import MenuItem
try:
    from wagtail.admin.rich_text import HalloPlugin
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin.rich_text import HalloPlugin
try:
    from wagtail.core import hooks
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore import hooks
try:
    from wagtail.core.models import Page
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.models import Page

from ask_cfpb.models import Answer, AnswerPage
from ask_cfpb.scripts import export_ask_data


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
    def create_sister_page(new_page, answer_base):
        sister_map = {
            'es': {
                'language': 'en',
                'parent': Page.objects.get(slug='ask-cfpb').specific,
                'title_prefix': 'English draft of',
            },
            'en': {
                'language': 'es',
                'parent': Page.objects.get(slug='obtener-respuestas').specific,
                'title_prefix': 'Spanish draft of',
            }
        }
        sister_values = sister_map[new_page.language]
        sister_page = AnswerPage(
            live=False,
            language=sister_values['language'],
            title="{} {}-{}-{}".format(
                sister_values['title_prefix'],
                new_page.title,
                sister_values['language'],
                answer_base.pk),
            answer_base=answer_base,
        )
        sister_values['parent'].add_child(instance=sister_page)
        return sister_page

    if isinstance(page, AnswerPage) and page.answer_base is None:
        new_answer_base = Answer(
            last_user=request.user,
            question=page.title)
        new_answer_base.save()
        new_id = new_answer_base.pk
        page.answer_base = new_answer_base
        page.language = page.get_parent().language
        sister_page = create_sister_page(page, new_answer_base)
        sister_page.save()
        sister_page.save_revision(user=request.user)
        page.title = "{}-{}-{}".format(
            page.title, page.language, new_id)
        page.slug = "{}-{}-{}".format(
            page.slug, page.language, new_id)
        page.save()
        page.save_revision(user=request.user)
