from __future__ import unicode_literals

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from ask_cfpb.models import (
    Answer,
    Audience,
    Category,
    NextStep,
    SubCategory)


class AnswerModelAdmin(ModelAdmin):
    model = Answer
    menu_label = 'Answers'
    menu_icon = 'list-ul'
    list_display = (
        'id', 'question', 'last_edited', 'question_es', 'last_edited_es')
    search_fields = (
        'id', 'question', 'question_es', 'answer', 'answer_es')
    list_filter = ('category',)


class AudienceModelAdmin(ModelAdmin):
    model = Audience
    menu_icon = 'list-ul'
    menu_label = 'Audiences'


class NextStepModelAdmin(ModelAdmin):
    model = NextStep
    menu_label = 'Next steps'
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
