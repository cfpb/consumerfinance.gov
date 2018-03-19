from django.conf.urls import url

from permissions_viewer import views


urlpatterns = [
    url(r'^user/([^\/]+)/',
        views.display_user_permissions,
        name='user'),
    url(r'^group/([^\/]+)/',
        views.display_group_roster,
        name='group'),
    url(r'^$',
        views.index,
        name='index'),
]
