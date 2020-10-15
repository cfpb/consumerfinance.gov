from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from search.elasticsearch_helpers import strip_html
from teachers_digital_platform.models.pages import ActivityPage
from teachers_digital_platform.models.django import (
    ActivityBloomsTaxonomyLevel,
    ActivityBuildingBlock, ActivityGradeLevel, ActivityAgeRange,
    ActivityStudentCharacteristics, ActivitySchoolSubject,
    ActivityTeachingStrategy, ActivityTopic, ActivityType,
    ActivityJumpStartCoalition, ActivityCouncilForEconEd
)


@registry.register_document
class ActivityPageDocument(Document):
    """Index an ActivityPage's fields and relations."""

    text = fields.TextField(attr='summary', boost=10)
    title = fields.TextField(attr='title', boost=10)
    date = fields.DateField(attr='date')
    big_idea = fields.TextField()
    essential_questions = fields.TextField()
    objectives = fields.TextField()
    what_students_will_do = fields.TextField()
    # MtM-related models:
    activity_type = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    age_range = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    blooms_taxonomy_level = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    building_block = fields.ObjectField(properties={
        'svg_icon': fields.TextField(),
        'pk': fields.TextField()
    })
    council_for_economic_education = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    grade_level = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    jump_start_coalition = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    school_subject = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    student_characteristics = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    teaching_strategy = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })
    # Foreign-key model:
    activity_duration = fields.ObjectField(properties={
        'title': fields.TextField(),
        'pk': fields.TextField()
    })

    class Index:
        name = 'teachers-digital-platform'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = ActivityPage
        related_models = [
            ActivityAgeRange,
            ActivityBloomsTaxonomyLevel,
            ActivityBuildingBlock,
            ActivityCouncilForEconEd,
            ActivityGradeLevel,
            ActivityJumpStartCoalition,
            ActivitySchoolSubject,
            ActivityStudentCharacteristics,
            ActivityTeachingStrategy,
            ActivityTopic,
            ActivityType,
        ]

    def get_queryset(self):
        """Prevent non-live pages from being indexed."""
        return super(
            ActivityPageDocument, self).get_queryset().filter(live=True)

    def prepare_big_idea(self, instance):
        return strip_html(instance.big_idea)

    def prepare_essential_questions(self, instance):
        return strip_html(instance.essential_questions)

    def prepare_objectives(self, instance):
        return strip_html(instance.objectives)

    def prepare_summary(self, instance):
        return strip_html(instance.summary)

    def prepare_what_students_will_do(self, instance):
        return strip_html(instance.what_students_will_do)

    def get_instances_from_related(self, related_instance):
        """
        Return querysets for MtM-related instances.

        To access the 'related_instance' parameter, we need to declare the
        MtM-related models in the 'related_models' value of the Django class.
        """
        return related_instance.all()
