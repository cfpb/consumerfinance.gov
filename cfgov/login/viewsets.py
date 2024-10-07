from wagtail.users.views.users import UserViewSet as WagtailUserViewSet

from login.forms import UserCreationForm, UserEditForm


class UserViewSet(WagtailUserViewSet):
    def get_form_class(self, for_update=False):
        if for_update:
            return UserEditForm
        return UserCreationForm
