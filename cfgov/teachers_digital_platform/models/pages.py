from django import forms
from django.db import models
from django.utils import timezone

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import RichTextField
from wagtail.models import Orderable

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from teachers_digital_platform.fields import ParentalTreeManyToManyField
from teachers_digital_platform.models.django import ActivityTopic
from v1.models import CFGOVPage


class ActivityPageActivityDocuments(Orderable):
    project = ParentalKey(
        "ActivityPage",
        on_delete=models.CASCADE,
        related_name="activity_documents",
    )

    documents = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Teacher guide",
    )

    panels = [FieldPanel("documents")]


class ActivityPageHandoutDocuments(Orderable):
    project = ParentalKey(
        "ActivityPage",
        on_delete=models.CASCADE,
        related_name="handout_documents",
    )

    documents = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Student file",
    )

    panels = [FieldPanel("documents")]


class ActivityPage(CFGOVPage):
    """A model for the Activity Detail page."""

    parent_page_types = ["ActivityIndexPage"]
    subpage_types = []

    date = models.DateField("Updated", default=timezone.now)
    summary = models.TextField("Summary", blank=False)
    big_idea = RichTextField("Big idea", blank=False)
    essential_questions = RichTextField("Essential questions", blank=False)
    objectives = RichTextField("Objectives", blank=False)
    what_students_will_do = RichTextField("What students will do", blank=False)  # noqa: E501
    search_tags = models.TextField(
        "Activity search tags",
        blank=True,
        help_text="These words will match for the site's internal"
        + " Activities search. This content will not be visible by users.",
    )
    activity_file = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Teacher guide",
    )
    # TODO: to figure out how to use Document choosers on ManyToMany fields
    handout_file = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Student file 1",
    )
    handout_file_2 = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Student file 2",
    )
    handout_file_3 = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Student file 3",
    )
    building_block = ParentalManyToManyField(
        "teachers_digital_platform.ActivityBuildingBlock", blank=False
    )  # noqa: E501
    school_subject = ParentalManyToManyField(
        "teachers_digital_platform.ActivitySchoolSubject", blank=False
    )  # noqa: E501
    topic = ParentalTreeManyToManyField(
        "teachers_digital_platform.ActivityTopic", blank=False
    )  # noqa: E501
    # Audience
    grade_level = ParentalManyToManyField(
        "teachers_digital_platform.ActivityGradeLevel", blank=False
    )  # noqa: E501
    age_range = ParentalManyToManyField(
        "teachers_digital_platform.ActivityAgeRange", blank=False
    )  # noqa: E501
    student_characteristics = ParentalManyToManyField(
        "teachers_digital_platform.ActivityStudentCharacteristics", blank=True
    )  # noqa: E501
    # Activity Characteristics
    activity_type = ParentalManyToManyField(
        "teachers_digital_platform.ActivityType", blank=False
    )  # noqa: E501
    teaching_strategy = ParentalManyToManyField(
        "teachers_digital_platform.ActivityTeachingStrategy", blank=False
    )  # noqa: E501
    blooms_taxonomy_level = ParentalManyToManyField(
        "teachers_digital_platform.ActivityBloomsTaxonomyLevel", blank=False
    )  # noqa: E501
    activity_duration = models.ForeignKey(
        "teachers_digital_platform.ActivityDuration",
        blank=False,
        on_delete=models.PROTECT,
    )  # noqa: E501
    # Standards taught
    jump_start_coalition = ParentalManyToManyField(
        "teachers_digital_platform.ActivityJumpStartCoalition",
        blank=True,
        verbose_name="Jump$tart Coalition",
    )
    council_for_economic_education = ParentalManyToManyField(
        "teachers_digital_platform.ActivityCouncilForEconEd",
        blank=True,
        verbose_name="National Standards",
    )
    content_panels = CFGOVPage.content_panels + [
        FieldPanel("date"),
        FieldPanel("summary"),
        FieldPanel("big_idea"),
        FieldPanel("essential_questions"),
        FieldPanel("objectives"),
        FieldPanel("what_students_will_do"),
        MultiFieldPanel(
            [
                FieldPanel("activity_file"),
                InlinePanel(
                    "activity_documents",
                    label="Additional activity files",
                    min_num=0,
                    max_num=5,
                ),
                FieldPanel("handout_file"),
                FieldPanel("handout_file_2"),
                FieldPanel("handout_file_3"),
                InlinePanel(
                    "handout_documents",
                    label="Additional handout files",
                    min_num=0,
                    max_num=10,
                ),
            ],
            heading="Download activity",
        ),
        FieldPanel("search_tags"),
        FieldPanel("building_block", widget=forms.CheckboxSelectMultiple),
        FieldPanel("topic", widget=forms.CheckboxSelectMultiple),
        FieldPanel("school_subject", widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel("grade_level", widget=forms.CheckboxSelectMultiple),  # noqa: E501
                FieldPanel("age_range", widget=forms.CheckboxSelectMultiple),
                FieldPanel(
                    "student_characteristics",
                    widget=forms.CheckboxSelectMultiple,
                ),  # noqa: E501
            ],
            heading="Audience",
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "activity_type", widget=forms.CheckboxSelectMultiple
                ),  # noqa: E501
                FieldPanel(
                    "teaching_strategy", widget=forms.CheckboxSelectMultiple
                ),  # noqa: E501
                FieldPanel(
                    "blooms_taxonomy_level",
                    widget=forms.CheckboxSelectMultiple,
                ),  # noqa: E501
                FieldPanel("activity_duration"),
            ],
            heading="Activity characteristics",
        ),
        FieldPanel(
            "council_for_economic_education",
            widget=forms.CheckboxSelectMultiple,
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "jump_start_coalition",
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading="Legacy unpublished data",
            classname="collapsible collapsed",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar/Footer"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "teachers_digital_platform/activity_page.html"

    def get_subtopic_ids(self):
        """Get a list of this activity's subtopic ids."""
        topic_ids = [topic.id for topic in self.topic.all()]
        root_ids = ActivityTopic.objects.filter(
            id__in=topic_ids, parent=None
        ).values_list("id", flat=True)
        return set(topic_ids) - set(root_ids)

    def get_grade_level_ids(self):
        """Get a list of this activity's grade_level ids."""
        grade_level_ids = [
            grade_level.id for grade_level in self.grade_level.all()
        ]
        return grade_level_ids

    def get_related_activities_url(self):
        """Generate a search url for related Activities."""
        parent_page = self.get_parent()
        subtopic_ids = [str(x) for x in self.get_subtopic_ids()]
        grade_level_ids = [str(y) for y in self.get_grade_level_ids()]

        url = parent_page.get_url() + "?q="
        if subtopic_ids:
            subtopics = "&topic=" + "&topic=".join(subtopic_ids)
            url += subtopics
        if grade_level_ids:
            grade_levels = "&grade_level=" + "&grade_level=".join(
                grade_level_ids
            )
            url += grade_levels
        return url

    def get_topics_list(self, parent=None):
        """
        Get a hierarchical list of this activity's topics.

        parent: ActivityTopic
        """
        if parent:
            descendants = set(parent.get_descendants()) & set(self.topic.all())
            children = parent.get_children()
            children_list = []
            # If this parent has descendants in self.topic, add its children.
            if descendants:
                for child in children:
                    if child in self.topic.all():
                        children_list.append(child.title)

                if children_list:
                    return parent.title + " (" + ", ".join(children_list) + ")"
            # Otherwise, just add the parent.
            else:
                return parent.title
        else:
            # Build root list of topics and recurse their children.
            topic_list = []
            topic_ids = [topic.id for topic in self.topic.all()]
            ancestors = ActivityTopic.objects.filter(
                id__in=topic_ids
            ).get_ancestors(True)
            roots = ActivityTopic.objects.filter(parent=None) & ancestors
            for root_topic in roots:
                topic_list.append(self.get_topics_list(root_topic))

            if topic_list:
                return ", ".join(topic_list)

    class Meta:
        verbose_name = "TDP Activity page"
