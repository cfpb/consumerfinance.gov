from __future__ import unicode_literals

from wagtail.contrib.modeladmin.options import modeladmin_register

from treemodeladmin.options import TreeModelAdmin

from regulations3k.models import EffectiveVersion, Part, Section, Subpart


class SectionModelAdmin(TreeModelAdmin):
    model = Section
    menu_label = 'Regulation section content'
    menu_icon = 'list-ul'
    list_display = (
        'title',
    )
    search_fields = (
        'label', 'title')
    parent_field = 'subpart'


class SubpartModelAdmin(TreeModelAdmin):
    model = Subpart
    menu_label = 'Regulation subpart'
    menu_icon = 'list-ul'
    list_display = (
        'title',
        'section_range',
    )
    child_field = 'sections'
    child_model_admin = SectionModelAdmin
    parent_field = 'version'


class EffectiveVersionModelAdmin(TreeModelAdmin):
    model = EffectiveVersion
    menu_label = 'Regulation effective versions'
    menu_icon = 'list-ul'
    list_display = (
        'effective_date',
        'draft',
        'acquired')
    child_field = 'subparts'
    child_model_admin = SubpartModelAdmin
    parent_field = 'part'


@modeladmin_register
class PartModelAdmin(TreeModelAdmin):
    model = Part
    menu_label = 'Regulations'
    menu_icon = 'list-ul'
    list_display = (
        'part_number',
        'title',
        'letter_code'
    )
    child_field = 'versions'
    child_model_admin = EffectiveVersionModelAdmin
