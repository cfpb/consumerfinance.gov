from haystack import indexes

from teachers_digital_platform.models import ActivityIndexPage, ActivityPage


class ActivityPageIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(
        document=True, use_template=True
    )
    date = indexes.DateTimeField(
        model_attr='date'
    )
    summary = indexes.CharField(
        model_attr='summary'
    )
    live = indexes.BooleanField(
        model_attr='live'
    )
    big_idea = indexes.CharField(
        model_attr='big_idea'
    )
    essential_questions = indexes.CharField(
        model_attr='essential_questions'
    )
    objectives = indexes.CharField(
        model_attr='objectives'
    )
    what_students_will_do = indexes.CharField(
        model_attr='what_students_will_do'
    )
    building_block = indexes.MultiValueField(
        model_attr='building_block', faceted=True
    )
    school_subject = indexes.MultiValueField(
        model_attr='school_subject', faceted=True
    )
    topic = indexes.MultiValueField(
        model_attr='topic', faceted=True
    )
    # Audience
    grade_level = indexes.MultiValueField(
        model_attr='grade_level', faceted=True
    )
    age_range = indexes.MultiValueField(
        model_attr='age_range', faceted=True
    )
    student_characteristics = indexes.MultiValueField(
        model_attr='student_characteristics', faceted=True
    )
    # Activity Characteristics
    activity_type = indexes.MultiValueField(
        model_attr='activity_type', faceted=True
    )
    teaching_strategy = indexes.MultiValueField(
        model_attr='teaching_strategy', faceted=True
    )
    blooms_taxonomy_level = indexes.MultiValueField(
        model_attr='blooms_taxonomy_level', faceted=True
    )
    activity_duration = indexes.CharField(
        model_attr='activity_duration', faceted=True
    )
    # Standards taught
    jump_start_coalition = indexes.MultiValueField(
        model_attr='jump_start_coalition', faceted=True
    )
    council_for_economic_education = indexes.MultiValueField(
        model_attr='council_for_economic_education', faceted=True
    )

    def prepare_building_block(self, obj):
        return [item.id for item in obj.building_block.all()]

    def prepare_school_subject(self, obj):
        return [item.id for item in obj.school_subject.all()]

    def prepare_topic(self, obj):
        return [item.id for item in obj.topic.all()]

    def prepare_grade_level(self, obj):
        return [item.id for item in obj.grade_level.all()]

    def prepare_age_range(self, obj):
        return [item.id for item in obj.age_range.all()]

    def prepare_student_characteristics(self, obj):
        return [item.id for item in obj.student_characteristics.all()]

    def prepare_activity_type(self, obj):
        return [item.id for item in obj.activity_type.all()]

    def prepare_teaching_strategy(self, obj):
        return [item.id for item in obj.teaching_strategy.all()]

    def prepare_blooms_taxonomy_level(self, obj):
        return [item.id for item in obj.blooms_taxonomy_level.all()]

    def prepare_activity_duration(self, obj):
        return obj.activity_duration.id

    def prepare_jump_start_coalition(self, obj):
        return [item.id for item in obj.jump_start_coalition.all()]

    def prepare_council_for_economic_education(self, obj):
        return [item.id for item in obj.council_for_economic_education.all()]

    def get_model(self):
        return ActivityPage

    def index_queryset(self, using=None):
        """Only index descendants of the Activity Search page"""
        # This is safe because ActivityIndexPage is a singleton
        search_page = ActivityIndexPage.objects.get()
        return self.get_model().objects.live().descendant_of(search_page)
