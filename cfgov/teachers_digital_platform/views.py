from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from teachers_digital_platform.models import (
    ActivityAgeRange,
    ActivityBloomsTaxonomyLevel,
    ActivityBuildingBlock,
    ActivityCouncilForEconEd,
    ActivityDuration,
    ActivityGradeLevel,
    ActivityJumpStartCoalition,
    ActivitySchoolSubject,
    ActivityStudentCharacteristics,
    ActivityTeachingStrategy,
    ActivityType,
)


class ActivityBuildingBlockViewSet(SnippetViewSet):
    model = ActivityBuildingBlock
    icon = "list-ul"
    menu_label = "Building Block"


class ActivitySchoolSubjectViewSet(SnippetViewSet):
    model = ActivitySchoolSubject
    icon = "list-ul"
    menu_label = "School Subject"


class ActivityGradeLevelViewSet(SnippetViewSet):
    model = ActivityGradeLevel
    icon = "list-ul"
    menu_label = "Grade level"


class ActivityAgeRangeViewSet(SnippetViewSet):
    model = ActivityAgeRange
    icon = "list-ul"
    menu_label = "Age range"


class ActivityStudentCharacteristicsViewSet(SnippetViewSet):
    model = ActivityStudentCharacteristics
    icon = "list-ul"
    menu_label = "Student characteristics"


class ActivityTypeViewSet(SnippetViewSet):
    model = ActivityType
    icon = "list-ul"
    menu_label = "Activity type"


class ActivityTeachingStrategyViewSet(SnippetViewSet):
    model = ActivityTeachingStrategy
    icon = "list-ul"
    menu_label = "Teaching strategy"


class ActivityBloomsTaxonomyLevelViewSet(SnippetViewSet):
    model = ActivityBloomsTaxonomyLevel
    icon = "list-ul"
    menu_label = "Bloom's taxonomy level"


class ActivityDurationtViewSet(SnippetViewSet):
    model = ActivityDuration
    icon = "list-ul"
    menu_label = "Activity duration"


class ActivityJumpStartCoalitionViewSet(SnippetViewSet):
    model = ActivityJumpStartCoalition
    icon = "list-ul"
    menu_label = "Jump$tart Coalition"


class ActivityCouncilForEconEdViewSet(SnippetViewSet):
    model = ActivityCouncilForEconEd
    icon = "list-ul"
    menu_label = "National standards"


class TDPViewSetGroup(SnippetViewSetGroup):
    items = (
        ActivityBuildingBlockViewSet,
        ActivitySchoolSubjectViewSet,
        ActivityGradeLevelViewSet,
        ActivityAgeRangeViewSet,
        ActivityStudentCharacteristicsViewSet,
        ActivityTypeViewSet,
        ActivityTeachingStrategyViewSet,
        ActivityBloomsTaxonomyLevelViewSet,
        ActivityDurationtViewSet,
        ActivityJumpStartCoalitionViewSet,
        ActivityCouncilForEconEdViewSet,
    )
    menu_icon = "list-ul"
    menu_label = "TDP Activity"
