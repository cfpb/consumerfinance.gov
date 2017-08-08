from __future__ import unicode_literals

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from data_research.models import MortgageDataConstant


class MortgageDataConstantModelAdmin(ModelAdmin):
    model = MortgageDataConstant
    menu_label = 'Mortgage performance constants'
    menu_icon = 'list-ul'
    list_display = (
        'name',
        'value',
        'note',
        'updated')


@modeladmin_register
class ResearchModelAdminGroup(ModelAdminGroup):
    menu_label = 'Data Research'
    menu_icon = 'list-ul'
    items = (MortgageDataConstantModelAdmin,)
