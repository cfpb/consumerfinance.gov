from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from wagtail.contrib.modeladmin.views import EditView

from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule

from ask_cfpb.models import (
    Answer,
    Audience,
    Category,
    NextStep,
    SubCategory)


class AnswerModelAdminSaveUserEditView(EditView):

    def save_instance_user(self):
        self.instance.last_user = self.request.user
        self.instance.save(skip_page_update=True)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.save_instance_user()
        return super(EditView, self).dispatch(request, *args, **kwargs)


class AnswerModelAdmin(ModelAdmin):
    model = Answer
    menu_label = 'Answers'
    menu_icon = 'list-ul'
    list_display = (
        'id',
        'question',
        'last_edited',
        'question_es',
        'last_edited_es')
    search_fields = (
        'id', 'question', 'question_es', 'answer', 'answer_es')
    list_filter = ('category', 'featured')
    edit_view_class = AnswerModelAdminSaveUserEditView


class AudienceModelAdmin(ModelAdmin):
    model = Audience
    menu_icon = 'list-ul'
    menu_label = 'Audiences'


class NextStepModelAdmin(ModelAdmin):
    model = NextStep
    menu_label = 'Related resources'
    menu_icon = 'list-ul'
    list_display = (
        'title', 'text')


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
        AnswerModelAdmin,
        AudienceModelAdmin,
        CategoryModelAdmin,
        SubCategoryModelAdmin,
        NextStepModelAdmin)


def editor_js():
    js_files = [
        'js/html_editor.js',
        'js/ask_cfpb_tips.js'
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('editHtmlButton');
            registerHalloPlugin('answermodule');
        </script>
        """
    )


def editor_css():
    return format_html(
        '<link rel="stylesheet" href="' +
        settings.STATIC_URL +
        'css/question_tips.css">')


def whitelister_element_rules():
    return {
        'aside': attribute_rule({'class': True}),
    }

hooks.register('insert_editor_js', editor_js)
hooks.register('insert_editor_css', editor_css)
hooks.register(
    'construct_whitelister_element_rules', whitelister_element_rules)
