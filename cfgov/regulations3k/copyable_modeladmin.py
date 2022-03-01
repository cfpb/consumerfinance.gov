from django.contrib.admin.utils import quote
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from wagtail.contrib.modeladmin.views import InstanceSpecificView

from treemodeladmin.helpers import TreeButtonHelper
from treemodeladmin.options import TreeModelAdmin
from treemodeladmin.views import TreeViewParentMixin


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


class CopyButtonHelper(TreeButtonHelper):
    def copy_button(self, pk):
        cn = "button button-small button-secondary"
        return {
            "url": self.url_helper.get_action_url("copy", quote(pk)),
            "label": "Copy",
            "classname": cn,
            "title": "Copy this {}".format(self.verbose_name),
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        if exclude is None:
            exclude = []

        usr = self.request.user
        ph = self.permission_helper
        pk = getattr(obj, self.opts.pk.attname)

        btns = super().get_buttons_for_obj(
            obj,
            exclude=exclude,
            classnames_add=classnames_add,
            classnames_exclude=classnames_exclude,
        )

        # Use the edit permission to double for copying
        if "copy" not in exclude and ph.user_can_edit_obj(usr, obj):
            btns.insert(-1, self.copy_button(pk))

        return btns


class CopyView(TreeViewParentMixin, InstanceSpecificView):
    @method_decorator(login_required)
    def dispatch(self, request, *arg, **kwargs):
        new_instance = self.model_admin.copy(self.instance)
        return redirect(self.url_helper.get_action_url("edit", quote(new_instance.pk)))


class CopyableModelAdmin(TreeModelAdmin):
    button_helper_class = CopyButtonHelper
    copy_view_class = CopyView

    def copy(self, instance):
        raise NotImplementedError(
            "The copy() method must be implemented for each model admin"
        )  # pragma: no cover

    def copy_view(self, request, instance_pk):
        return self.copy_view_class.as_view(model_admin=self, instance_pk=instance_pk)(
            request
        )

    def get_admin_urls_for_registration(self, parent=None):
        urls = super(CopyableModelAdmin, self).get_admin_urls_for_registration()

        # Add the copy URL
        urls = urls + (
            re_path(
                self.url_helper.get_action_url_pattern("copy"),
                self.copy_view,
                name=self.url_helper.get_action_url_name("copy"),
            ),
        )

        return urls
