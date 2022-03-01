from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from data_research.models import MortgageDataConstant, MortgageMetaData


class MortgageMetaDataModelAdmin(ModelAdmin):
    model = MortgageMetaData
    menu_label = "Mortgage metadata"
    menu_icon = "list-ul"
    list_display = ("name", "json_value", "note", "updated")


class MortgageDataConstantModelAdmin(ModelAdmin):
    model = MortgageDataConstant
    menu_label = "Mortgage performance constants"
    menu_icon = "list-ul"
    list_display = ("name", "value", "date_value", "updated")


@modeladmin_register
class ResearchModelAdminGroup(ModelAdminGroup):
    menu_label = "Data Research"
    menu_icon = "list-ul"
    items = (MortgageDataConstantModelAdmin, MortgageMetaDataModelAdmin)
