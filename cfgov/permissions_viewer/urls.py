from permissions_viewer import views


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(r"^user/([^\/]+)/", views.display_user_permissions, name="user"),
    re_path(r"^group/([^\/]+)/", views.display_group_roster, name="group"),
    re_path(r"^$", views.index, name="index"),
]
