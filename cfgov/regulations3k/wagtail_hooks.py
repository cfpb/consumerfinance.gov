from __future__ import unicode_literals

from datetime import date

from wagtail.contrib.modeladmin.options import modeladmin_register

from treemodeladmin.options import TreeModelAdmin

from regulations3k.copyable_modeladmin import CopyableModelAdmin
from regulations3k.models import EffectiveVersion, Part, Section, Subpart


class SectionModelAdmin(TreeModelAdmin):
    model = Section
    menu_label = 'Regulation section content'
    menu_icon = 'list-ul'
    list_display = (
        'label', 'title',
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
        'section_range'
    )
    child_field = 'sections'
    child_model_admin = SectionModelAdmin
    parent_field = 'version'
    ordering = ['subpart_type', 'title']


class EffectiveVersionModelAdmin(CopyableModelAdmin):
    model = EffectiveVersion
    menu_label = 'Regulation effective versions'
    menu_icon = 'list-ul'
    list_display = (
        'effective_date',
        'status',
        'created')
    child_field = 'subparts'
    child_model_admin = SubpartModelAdmin
    parent_field = 'part'

    def copy(self, instance):
        # Create a new instance
        new_version = EffectiveVersion(
            authority=instance.authority,
            source=instance.source,
            part=instance.part,
            effective_date=date.today(),
            acquired=date.today(),
            draft=True,
        )
        new_version.save()

        # Copy subparts and sections
        for subpart in instance.subparts.all():
            sections = subpart.sections.all()
            new_subpart = subpart
            new_subpart.pk = None
            new_subpart.version = new_version
            new_subpart.save()

            for section in sections:
                new_section = section
                new_section.pk = None
                new_section.subpart = new_subpart
                new_section.save()

        return new_version


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
