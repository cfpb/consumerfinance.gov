from datetime import date

from django.utils.encoding import force_text

from wagtail.contrib.modeladmin.options import modeladmin_register

from treemodeladmin.helpers import TreeAdminURLHelper
from treemodeladmin.options import TreeModelAdmin
from treemodeladmin.views import TreeIndexView

from regulations3k.copyable_modeladmin import CopyableModelAdmin
from regulations3k.models import EffectiveVersion, Part, Section, Subpart


class RegsURLHelper(TreeAdminURLHelper):

    def crumb(
        self, parent_field=None, parent_instance=None, specific_instance=None
    ):
        """ Override the URL helper's crumb method to shorten reg model crumbs.

        The regulation models include their "parent" model's string
        representation within their own string representation. This is useful
        when referencing a model without context, but not so useful in
        breadcrumbs. This method will remove the "[Parent], " from the string
        if the specific_instance and parent_instance are provided.
        """
        index_url, crumb_text = super().crumb(
            parent_field=parent_field,
            parent_instance=parent_instance,
            specific_instance=specific_instance
        )

        if specific_instance is not None and parent_instance is not None:
            crumb_text = force_text(specific_instance).replace(
                force_text(parent_instance) + ", ",
                ""
            )

        return (index_url, crumb_text)


class SectionPreviewIndexView(TreeIndexView):

    def get_buttons_for_obj(self, obj):
        btns = self.button_helper.get_buttons_for_obj(
            obj, classnames_add=['button-small', 'button-secondary'])

        effective_version = obj.subpart.version
        date_str = effective_version.effective_date.isoformat()
        part = obj.subpart.version.part
        page = part.page.first()

        if page is not None:
            if effective_version.draft:
                label = 'View draft'
            else:
                label = 'View live'

            preview_url = page.url + page.reverse_subpage(
                'section',
                kwargs={'date_str': date_str, 'section_label': obj.url_path}
            )
            preview_button = {
                'url': preview_url,
                'label': label,
                'classname': 'button button-small button-secondary',
                'title': 'Preview this {}'.format(self.verbose_name),
            }
            btns.insert(-1, preview_button)

        return btns


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
    index_view_class = SectionPreviewIndexView
    url_helper_class = RegsURLHelper


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
    url_helper_class = RegsURLHelper


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
    url_helper_class = RegsURLHelper

    def copy(self, instance):
        subparts = instance.subparts.all()

        # Copy the instance
        new_version = instance
        new_version.pk = None
        new_version.created = date.today()
        new_version.draft = True
        new_version.save()

        for subpart in subparts:
            sections = subpart.sections.all()

            # Copy the subpart
            new_subpart = subpart
            new_subpart.pk = None
            new_subpart.version = new_version
            new_subpart.save()

            for section in sections:
                # Copy the section
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
        'short_name'
    )
    child_field = 'versions'
    child_model_admin = EffectiveVersionModelAdmin
    url_helper_class = RegsURLHelper
