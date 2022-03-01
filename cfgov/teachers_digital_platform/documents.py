from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from search.elasticsearch_helpers import environment_specific_index, strip_html
from teachers_digital_platform.models.pages import ActivityPage


mtm_fields = [
    "building_block",
    "school_subject",
    "topic",
    "grade_level",
    "age_range",
    "student_characteristics",
    "activity_type",
    "teaching_strategy",
    "blooms_taxonomy_level",
    "jump_start_coalition",
    "council_for_economic_education",
]


@registry.register_document
class ActivityPageDocument(Document):
    """Index an ActivityPage's fields and relations."""

    text = fields.TextField(attr="summary", boost=10)
    title = fields.TextField(attr="title", boost=10)
    date = fields.DateField(attr="date")
    big_idea = fields.TextField()
    essential_questions = fields.TextField()
    objectives = fields.TextField()
    what_students_will_do = fields.TextField()
    related_text = fields.TextField()
    # Foreign-key field:
    activity_duration = fields.KeywordField()
    # MTM fields
    activity_type = fields.KeywordField()
    age_range = fields.KeywordField()
    blooms_taxonomy_level = fields.KeywordField()
    building_block = fields.KeywordField()
    council_for_economic_education = fields.KeywordField()
    grade_level = fields.KeywordField()
    jump_start_coalition = fields.KeywordField()
    school_subject = fields.KeywordField()
    student_characteristics = fields.KeywordField()
    teaching_strategy = fields.KeywordField()
    topic = fields.KeywordField()

    class Index:
        name = environment_specific_index("teachers-digital-platform")
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = ActivityPage
        fields = ["id"]

    def get_queryset(self):
        """Prevent non-live pages from being indexed."""
        return super(ActivityPageDocument, self).get_queryset().filter(live=True)

    def prepare_activity_duration(self, instance):
        if instance.activity_duration:
            return instance.activity_duration.pk

    def prepare_activity_type(self, instance):
        if instance.activity_type:
            return [i.pk for i in instance.activity_type.all()]

    def prepare_age_range(self, instance):
        if instance.age_range:
            return [i.pk for i in instance.age_range.all()]

    def prepare_blooms_taxonomy_level(self, instance):
        if instance.blooms_taxonomy_level:
            return [i.pk for i in instance.blooms_taxonomy_level.all()]

    def prepare_building_block(self, instance):
        if instance.building_block:
            return [i.pk for i in instance.building_block.all()]

    def prepare_council_for_economic_education(self, instance):
        if instance.council_for_economic_education:
            return [i.pk for i in instance.council_for_economic_education.all()]

    def prepare_grade_level(self, instance):
        if instance.grade_level:
            return [i.pk for i in instance.grade_level.all()]

    def prepare_jump_start_coalition(self, instance):
        if instance.jump_start_coalition:
            return [i.pk for i in instance.jump_start_coalition.all()]

    def prepare_school_subject(self, instance):
        if instance.school_subject:
            return [i.pk for i in instance.school_subject.all()]

    def prepare_student_characteristics(self, instance):
        if instance.student_characteristics:
            return [i.pk for i in instance.student_characteristics.all()]

    def prepare_teaching_strategy(self, instance):
        if instance.teaching_strategy:
            return [i.pk for i in instance.teaching_strategy.all()]

    def prepare_topic(self, instance):
        if instance.topic:
            return [i.pk for i in instance.topic.all()]

    def prepare_related_text(self, instance):
        content_bits = []
        if instance.activity_duration:
            content_bits.append(instance.activity_duration.title)
        for field in mtm_fields:
            content_bits += [entry.title for entry in getattr(instance, field).all()]
        return " ".join(content_bits)

    def prepare_big_idea(self, instance):
        return strip_html(instance.big_idea)

    def prepare_essential_questions(self, instance):
        return strip_html(instance.essential_questions)

    def prepare_objectives(self, instance):
        return strip_html(instance.objectives)

    def prepare_what_students_will_do(self, instance):
        return strip_html(instance.what_students_will_do)
