from django.contrib.admin.utils import quote
from django.utils.translation import ugettext as _

from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from mega_menu.models import Menu
from mega_menu.views import MenuPreviewView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


class MenuModelAdminButtonHelper(ButtonHelper):
    def preview_button(self, pk, classnames_add=None, classnames_exclude=None):
        return {
            'url': self.url_helper.get_action_url('preview', quote(pk)),
            'label': _('Preview'),
            'classname': self.finalise_classname(
                classnames_add or [],
                classnames_exclude or []
            ),
            'title': _('Preview this %s') % self.verbose_name,
            'target': "_blank",
            'rel': 'noopener noreferrer',
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
                            classnames_exclude=None):
        buttons = super().get_buttons_for_obj(
            obj,
            exclude=exclude,
            classnames_add=classnames_add,
            classnames_exclude=classnames_exclude
        )

        buttons.append(
            self.preview_button(
                getattr(obj, self.opts.pk.attname),
                classnames_add,
                classnames_exclude
            )
        )

        return buttons


@modeladmin_register
class MenuModelAdmin(ModelAdmin):
    model = Menu
    menu_icon = 'list-ul'
    menu_label = 'Mega menu'
    button_helper_class = MenuModelAdminButtonHelper

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()

        return urls + (
            re_path(
                self.url_helper.get_action_url_pattern('preview'),
                self.preview_view,
                name=self.url_helper.get_action_url_name('preview')
            ),
        )

    def preview_view(self, request, instance_pk):
        return MenuPreviewView.as_view(
            model_admin=self,
            language=instance_pk
        )(request)

    def get_preview_template(self):
        return self.get_templates('preview')
