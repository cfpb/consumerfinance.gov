# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.utils import timezone

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.search import index

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from teachers_digital_platform.fields import ParentalTreeManyToManyField
from teachers_digital_platform.models.django import ActivityTopic
from v1.models import CFGOVPage, CFGOVPageManager


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

    panels = [DocumentChooserPanel("documents")]


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

    panels = [DocumentChooserPanel("documents")]


class ActivityPage(CFGOVPage):
    """A model for the Activity Detail page."""

    # Allow Activity pages to exist under the ActivityIndexPage or the Trash
    parent_page_types = ["ActivityIndexPage", "v1.HomePage"]
    subpage_types = []
    objects = CFGOVPageManager()

    date = models.DateField("Updated", default=timezone.now)
    summary = models.TextField("Summary", blank=False)
    big_idea = RichTextField("Big idea", blank=False)
    essential_questions = RichTextField("Essential questions", blank=False)
    objectives = RichTextField("Objectives", blank=False)
    what_students_will_do = RichTextField(
        "What students will do", blank=False
    )  # noqa: B950
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
    )  # noqa: B950
    school_subject = ParentalManyToManyField(
        "teachers_digital_platform.ActivitySchoolSubject", blank=False
    )  # noqa: B950
    topic = ParentalTreeManyToManyField(
        "teachers_digital_platform.ActivityTopic", blank=False
    )  # noqa: B950
    # Audience
    grade_level = ParentalManyToManyField(
        "teachers_digital_platform.ActivityGradeLevel", blank=False
    )  # noqa: B950
    age_range = ParentalManyToManyField(
        "teachers_digital_platform.ActivityAgeRange", blank=False
    )  # noqa: B950
    student_characteristics = ParentalManyToManyField(
        "teachers_digital_platform.ActivityStudentCharacteristics", blank=True
    )  # noqa: B950
    # Activity Characteristics
    activity_type = ParentalManyToManyField(
        "teachers_digital_platform.ActivityType", blank=False
    )  # noqa: B950
    teaching_strategy = ParentalManyToManyField(
        "teachers_digital_platform.ActivityTeachingStrategy", blank=False
    )  # noqa: B950
    blooms_taxonomy_level = ParentalManyToManyField(
        "teachers_digital_platform.ActivityBloomsTaxonomyLevel", blank=False
    )  # noqa: B950
    activity_duration = models.ForeignKey(
        "teachers_digital_platform.ActivityDuration",
        blank=False,
        on_delete=models.PROTECT,
    )  # noqa: B950
    # Standards taught
    jump_start_coalition = ParentalManyToManyField(
        "teachers_digital_platform.ActivityJumpStartCoalition",
        blank=True,
        verbose_name="Jump$tart Coalition",
    )
    council_for_economic_education = ParentalManyToManyField(
        "teachers_digital_platform.ActivityCouncilForEconEd",
        blank=True,
        verbose_name="Council for Economic Education",
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
                DocumentChooserPanel("activity_file"),
                InlinePanel(
                    "activity_documents",
                    label="Additional activity files",
                    min_num=0,
                    max_num=5,
                ),
                DocumentChooserPanel("handout_file"),
                DocumentChooserPanel("handout_file_2"),
                DocumentChooserPanel("handout_file_3"),
                InlinePanel(
                    "handout_documents",
                    label="Additional handout files",
                    min_num=0,
                    max_num=10,
                ),
            ],
            heading="Download activity",
        ),
        FieldPanel("building_block", widget=forms.CheckboxSelectMultiple),
        FieldPanel("school_subject", widget=forms.CheckboxSelectMultiple),
        FieldPanel("topic", widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel(
                    "grade_level", widget=forms.CheckboxSelectMultiple
                ),  # noqa: B950
                FieldPanel("age_range", widget=forms.CheckboxSelectMultiple),
                FieldPanel(
                    "student_characteristics",
                    widget=forms.CheckboxSelectMultiple,
                ),  # noqa: B950
            ],
            heading="Audience",
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "activity_type", widget=forms.CheckboxSelectMultiple
                ),  # noqa: B950
                FieldPanel(
                    "teaching_strategy", widget=forms.CheckboxSelectMultiple
                ),  # noqa: B950
                FieldPanel(
                    "blooms_taxonomy_level",
                    widget=forms.CheckboxSelectMultiple,
                ),  # noqa: B950
                FieldPanel("activity_duration"),
            ],
            heading="Activity characteristics",
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "council_for_economic_education",
                    widget=forms.CheckboxSelectMultiple,
                ),  # noqa: B950
                FieldPanel(
                    "jump_start_coalition", widget=forms.CheckboxSelectMultiple
                ),  # noqa: B950
            ],
            heading="National standards",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar/Footer"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    # admin use only
    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("big_idea"),
        index.SearchField("essential_questions"),
        index.SearchField("objectives"),
        index.SearchField("what_students_will_do"),
        index.FilterField("date"),
        index.FilterField("building_block"),
        index.FilterField("school_subject"),
        index.FilterField("topic"),
        index.FilterField("grade_level"),
        index.FilterField("age_range"),
        index.FilterField("student_characteristics"),
        index.FilterField("activity_type"),
        index.FilterField("teaching_strategy"),
        index.FilterField("blooms_taxonomy_level"),
        index.FilterField("activity_duration"),
        index.FilterField("jump_start_coalition"),
        index.FilterField("council_for_economic_education"),
    ]

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
