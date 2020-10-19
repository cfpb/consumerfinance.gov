from django.contrib import admin

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from mptt.admin import DraggableMPTTAdmin

from teachers_digital_platform.models import (
    ActivityAgeRange, ActivityBloomsTaxonomyLevel, ActivityBuildingBlock,
    ActivityCouncilForEconEd, ActivityDuration, ActivityGradeLevel,
    ActivityJumpStartCoalition, ActivitySchoolSubject,
    ActivityStudentCharacteristics, ActivityTeachingStrategy, ActivityTopic,
    ActivityType
)


class ActivityBuildingBlockModelAdmin(ModelAdmin):
    model = ActivityBuildingBlock
    menu_label = 'Building Block'
    menu_icon = 'list-ul'


class ActivitySchoolSubjectModelAdmin(ModelAdmin):
    model = ActivitySchoolSubject
    menu_icon = 'list-ul'
    menu_label = 'School Subject'


class ActivityTopicModelAdmin(DraggableMPTTAdmin):
    model = ActivityTopic
    menu_icon = 'list-ul'
    menu_label = 'Topic'


admin.site.register(ActivityTopic, ActivityTopicModelAdmin)


class ActivityGradeLevelModelAdmin(ModelAdmin):
    model = ActivityGradeLevel
    menu_icon = 'list-ul'
    menu_label = 'Grade level'


class ActivityAgeRangeModelAdmin(ModelAdmin):
    model = ActivityAgeRange
    menu_icon = 'list-ul'
    menu_label = 'Age range'


class ActivityStudentCharacteristicsModelAdmin(ModelAdmin):
    model = ActivityStudentCharacteristics
    menu_icon = 'list-ul'
    menu_label = 'Student characteristics'


class ActivityTypeModelAdmin(ModelAdmin):
    model = ActivityType
    menu_icon = 'list-ul'
    menu_label = 'Activity type'


class ActivityTeachingStrategyModelAdmin(ModelAdmin):
    model = ActivityTeachingStrategy
    menu_icon = 'list-ul'
    menu_label = 'Teaching strategy'


class ActivityBloomsTaxonomyLevelModelAdmin(ModelAdmin):
    model = ActivityBloomsTaxonomyLevel
    menu_icon = 'list-ul'
    menu_label = 'Bloom\'s taxonomy level'


class ActivityDurationtModelAdmin(ModelAdmin):
    model = ActivityDuration
    menu_icon = 'list-ul'
    menu_label = 'Activity duration'


class ActivityJumpStartCoalitionModelAdmin(ModelAdmin):
    model = ActivityJumpStartCoalition
    menu_icon = 'list-ul'
    menu_label = 'Jump$tart Coalition'


class ActivityCouncilForEconEdModelAdmin(ModelAdmin):
    model = ActivityCouncilForEconEd
    menu_icon = 'list-ul'
    menu_label = 'Council for Economic Education'


@modeladmin_register
class MyModelAdminGroup(ModelAdminGroup):
    menu_label = 'TDP Activity'
    menu_icon = 'list-ul'
    items = (
        ActivityBuildingBlockModelAdmin,
        ActivitySchoolSubjectModelAdmin,
        ActivityGradeLevelModelAdmin,
        ActivityAgeRangeModelAdmin,
        ActivityStudentCharacteristicsModelAdmin,
        ActivityTypeModelAdmin,
        ActivityTeachingStrategyModelAdmin,
        ActivityBloomsTaxonomyLevelModelAdmin,
        ActivityDurationtModelAdmin,
        ActivityJumpStartCoalitionModelAdmin,
        ActivityCouncilForEconEdModelAdmin,
    )
