from django.contrib import admin

from wagtail.snippets.models import register_snippet

from mptt.admin import DraggableMPTTAdmin

from teachers_digital_platform.models import ActivityTopic
from teachers_digital_platform.views import TDPViewSetGroup


class ActivityTopicModelAdmin(DraggableMPTTAdmin):
    model = ActivityTopic
    menu_icon = "list-ul"
    menu_label = "Topic"


admin.site.register(ActivityTopic, ActivityTopicModelAdmin)


register_snippet(TDPViewSetGroup)
