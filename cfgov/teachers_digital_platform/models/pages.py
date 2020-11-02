# -*- coding: utf-8 -*-
from django import forms
from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.utils import timezone
from haystack.query import SearchQuerySet

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.search import index

from modelcluster.fields import ParentalManyToManyField

from teachers_digital_platform.fields import ParentalTreeManyToManyField
from teachers_digital_platform.models import (
    ActivityAgeRange, ActivityBloomsTaxonomyLevel, ActivityBuildingBlock,
    ActivityCouncilForEconEd, ActivityDuration, ActivityGradeLevel,
    ActivityJumpStartCoalition, ActivitySchoolSubject,
    ActivityStudentCharacteristics, ActivityTeachingStrategy, ActivityTopic,
    ActivityType
)
from teachers_digital_platform.molecules import TdpSearchHeroImage
from v1.atomic_elements import molecules
from v1.models import CFGOVPage, CFGOVPageManager, HomePage


class ActivityIndexPage(CFGOVPage):
    """
    A model for the Activity Search page.
    """

    subpage_types = ['teachers_digital_platform.ActivityPage']

    objects = CFGOVPageManager()

    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('notification', molecules.Notification()),
    ], blank=True)

    header_sidebar = StreamField([
        ('image', TdpSearchHeroImage()),
    ], blank=True)

    results = {}
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('header_sidebar'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar/Footer'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(ActivityIndexPage, cls).can_create_at(parent) \
            and not cls.objects.exists()

    def get_template(self, request):
        template = 'teachers_digital_platform/activity_index_page.html'
        if 'partial' in request.GET:
            template = 'teachers_digital_platform/activity_search_facets_and_results.html'  # noqa: E501
        return template

    def get_context(self, request, *args, **kwargs):
        facet_map = (
            ('building_block', (ActivityBuildingBlock, False, 10)),
            ('school_subject', (ActivitySchoolSubject, False, 25)),
            ('topic', (ActivityTopic, True, 25)),
            ('grade_level', (ActivityGradeLevel, False, 10)),
            ('age_range', (ActivityAgeRange, False, 10)),
            ('student_characteristics', (ActivityStudentCharacteristics, False, 10)),  # noqa: E501
            ('activity_type', (ActivityType, False, 10)),
            ('teaching_strategy', (ActivityTeachingStrategy, False, 25)),
            ('blooms_taxonomy_level', (ActivityBloomsTaxonomyLevel, False, 25)),  # noqa: E501
            ('activity_duration', (ActivityDuration, False, 10)),
            ('jump_start_coalition', (ActivityJumpStartCoalition, False, 25)),
            ('council_for_economic_education', (ActivityCouncilForEconEd, False, 25)),  # noqa: E501
        )
        search_query = request.GET.get('q', '')  # haystack cleans this string
        sqs = SearchQuerySet().models(ActivityPage).filter(live=True)
        total_activities = sqs.count()
        # Load selected facets
        selected_facets = {}
        facet_queries = {}

        for facet, facet_config in facet_map:
            sqs = sqs.facet(str(facet), size=facet_config[2])
            if facet in request.GET and request.GET.get(facet):
                selected_facets[facet] = [
                    int(value) for value in request.GET.getlist(facet)
                    if value.isdigit()
                ]
                facet_queries[facet] = facet + '_exact:' + (
                    " OR " + facet + "_exact:").join(
                    [str(value) for value in selected_facets[facet]]
                )

        payload = {
            'search_query': search_query,
            'results': [],
            'total_results': 0,
            'total_activities': total_activities,
            'selected_facets': selected_facets,
            'facet_queries': facet_queries,
            'all_facets': {},
        }

        # Apply search query if it exists, but don't apply facets
        if search_query:
            sqs = sqs.filter(content=search_query).order_by('-_score', '-date')  # noqa: E501
        else:
            sqs = sqs.order_by('-date')

        # Get all facets and their counts
        facet_counts = sqs.facet_counts()
        all_facets = self.get_all_facets(facet_map, sqs, facet_counts, facet_queries, selected_facets)  # noqa: E501

        # List all facet blocks that need to be expanded
        always_expanded = {'building_block', 'topic', 'school_subject'}
        conditionally_expanded = {
            facet_name for facet_name, facet_items in all_facets.items()
            if any(
                facet['selected'] is True for facet in facet_items
            )
        }
        expanded_facets = always_expanded.union(set(conditionally_expanded))

        payload.update({
            'facet_counts': facet_counts,
            'all_facets': all_facets,
            'expanded_facets': expanded_facets,
        })

        # Apply all the active facet values to our search results
        for facet_narrow_query in facet_queries.values():
            sqs = sqs.narrow(facet_narrow_query)

        results = [activity.object for activity in sqs]
        total_results = sqs.count()

        payload.update({
            'results': results,
            'total_results': total_results,
        })
        self.results = payload
        results_per_page = validate_results_per_page(request)
        paginator = Paginator(payload['results'], results_per_page)
        current_page = validate_page_number(request, paginator)
        paginated_page = paginator.page(current_page)

        context = super(ActivityIndexPage, self).get_context(request)
        context.update({
            'facet_counts': facet_counts,
            'facets': all_facets,
            'activities': paginated_page,
            'total_results': total_results,
            'results_per_page': results_per_page,
            'current_page': current_page,
            'paginator': paginator,
            'show_filters': bool(facet_queries),
        })
        return context

    def get_all_facets(self, facet_map, sqs, facet_counts, facet_queries, selected_facets):  # noqa: E501
        all_facets = {}
        if 'fields' in facet_counts:
            for facet, facet_config in facet_map:
                class_object, is_nested, max_facet_count = facet_config
                all_facets_sqs = sqs
                other_facet_queries = [
                    facet_query for facet_query_name, facet_query in facet_queries.items()  # noqa: E501
                    if facet != facet_query_name
                ]
                for other_facet_query in other_facet_queries:
                    all_facets_sqs = all_facets_sqs.narrow(str(other_facet_query))  # noqa: E501
                narrowed_facet_counts = all_facets_sqs.facet_counts()
                if 'fields' in narrowed_facet_counts and facet in narrowed_facet_counts['fields']:  # noqa: E501
                    narrowed_facets = [value[0] for value in narrowed_facet_counts['fields'][facet]]  # noqa: E501
                    narrowed_selected_facets = selected_facets[facet] if facet in selected_facets else []  # noqa: E501
                    if is_nested:
                        all_facets[facet] = self.get_nested_facets(
                            class_object,
                            narrowed_facets,
                            narrowed_selected_facets
                        )
                    else:
                        all_facets[facet] = self.get_flat_facets(
                            class_object,
                            narrowed_facets,
                            narrowed_selected_facets
                        )
        return all_facets

    def get_flat_facets(self, class_object, narrowed_facets, selected_facets):
        final_facets = [
            {
                'selected': result['id'] in selected_facets,
                'id': result['id'],
                'title': result['title'],
            } for result in class_object.objects.filter(pk__in=narrowed_facets).values('id', 'title')]  # noqa: E501
        return final_facets

    def get_nested_facets(self, class_object, narrowed_facets, selected_facets, parent=None):  # noqa: E501
        if not parent:
            flat_final_facets = [
                {
                    'selected': result['id'] in selected_facets,
                    'id': result['id'],
                    'title': result['title'],
                    'parent': result['parent'],
                } for result in class_object.objects.filter(pk__in=narrowed_facets).get_ancestors(True).values('id', 'title', 'parent')]  # noqa: E501
            final_facets = []
            root_facets = [root_facet for root_facet in flat_final_facets if root_facet['parent'] is None]  # noqa: E501
            for root_facet in root_facets:
                children_list = self.get_nested_facets(class_object, narrowed_facets, selected_facets, root_facet['id'])  # noqa: E501
                child_selected = any(
                    child['selected'] is True or child['child_selected'] is True for child in children_list  # noqa: E501
                )
                final_facets.append(
                    {
                        'selected': root_facet['selected'],
                        'child_selected': child_selected,
                        'id': root_facet['id'],
                        'title': root_facet['title'],
                        'parent': root_facet['parent'],
                        'children': children_list
                    })
            return final_facets
        else:
            children = [
                {
                    'selected': result['id'] in selected_facets or result['parent'] in selected_facets,  # noqa: E501
                    'id': result['id'],
                    'title': result['title'],
                    'parent': result['parent'],
                    'children': self.get_nested_facets(class_object, narrowed_facets, selected_facets, result['id']),  # noqa: E501
                    'child_selected': any(
                        child['selected'] is True or child['child_selected'] is True for child in  # noqa: E501
                        self.get_nested_facets(class_object, narrowed_facets, selected_facets, result['id'])  # noqa: E501
                    )
                } for result in class_object.objects.filter(pk__in=narrowed_facets).filter(parent_id=parent).values('id', 'title', 'parent')]  # noqa: E501
            return children

    class Meta:
        verbose_name = "TDP Activity search page"


class ActivityPage(CFGOVPage):
    """
    A model for the Activity Detail page.
    """
    # Allow Activity pages to exist under the ActivityIndexPage or the Trash
    parent_page_types = [ActivityIndexPage, HomePage]
    subpage_types = []
    objects = CFGOVPageManager()

    date = models.DateField('Updated', default=timezone.now)
    summary = models.TextField('Summary', blank=False)
    big_idea = RichTextField('Big idea', blank=False)
    essential_questions = RichTextField('Essential questions', blank=False)
    objectives = RichTextField('Objectives', blank=False)
    what_students_will_do = RichTextField('What students will do', blank=False)  # noqa: E501
    activity_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Teacher guide'
    )
    # TODO: to figure out how to use Document choosers on ManyToMany fields
    handout_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Student file 1'
    )
    handout_file_2 = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Student file 2'
    )
    handout_file_3 = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Student file 3'
    )
    building_block = ParentalManyToManyField('teachers_digital_platform.ActivityBuildingBlock', blank=False)  # noqa: E501
    school_subject = ParentalManyToManyField('teachers_digital_platform.ActivitySchoolSubject', blank=False)  # noqa: E501
    topic = ParentalTreeManyToManyField('teachers_digital_platform.ActivityTopic', blank=False)  # noqa: E501
    # Audience
    grade_level = ParentalManyToManyField('teachers_digital_platform.ActivityGradeLevel', blank=False)  # noqa: E501
    age_range = ParentalManyToManyField('teachers_digital_platform.ActivityAgeRange', blank=False)  # noqa: E501
    student_characteristics = ParentalManyToManyField('teachers_digital_platform.ActivityStudentCharacteristics', blank=True)  # noqa: E501
    # Activity Characteristics
    activity_type = ParentalManyToManyField('teachers_digital_platform.ActivityType', blank=False)  # noqa: E501
    teaching_strategy = ParentalManyToManyField('teachers_digital_platform.ActivityTeachingStrategy', blank=False)  # noqa: E501
    blooms_taxonomy_level = ParentalManyToManyField('teachers_digital_platform.ActivityBloomsTaxonomyLevel', blank=False)  # noqa: E501
    activity_duration = models.ForeignKey(ActivityDuration, blank=False, on_delete=models.PROTECT)  # noqa: E501
    # Standards taught
    jump_start_coalition = ParentalManyToManyField(
        'teachers_digital_platform.ActivityJumpStartCoalition',
        blank=True,
        verbose_name='Jump$tart Coalition',
    )
    council_for_economic_education = ParentalManyToManyField(
        'teachers_digital_platform.ActivityCouncilForEconEd',
        blank=True,
        verbose_name='Council for Economic Education',
    )
    content_panels = CFGOVPage.content_panels + [
        FieldPanel('date'),
        FieldPanel('summary'),
        FieldPanel('big_idea'),
        FieldPanel('essential_questions'),
        FieldPanel('objectives'),
        FieldPanel('what_students_will_do'),
        MultiFieldPanel(
            [
                DocumentChooserPanel('activity_file'),
                DocumentChooserPanel('handout_file'),
                DocumentChooserPanel('handout_file_2'),
                DocumentChooserPanel('handout_file_3'),
            ],
            heading="Download activity",
        ),
        FieldPanel('building_block', widget=forms.CheckboxSelectMultiple),
        FieldPanel('school_subject', widget=forms.CheckboxSelectMultiple),
        FieldPanel('topic', widget=forms.CheckboxSelectMultiple),

        MultiFieldPanel(
            [
                FieldPanel('grade_level', widget=forms.CheckboxSelectMultiple),  # noqa: E501
                FieldPanel('age_range', widget=forms.CheckboxSelectMultiple),
                FieldPanel('student_characteristics', widget=forms.CheckboxSelectMultiple),  # noqa: E501
            ],
            heading="Audience",
        ),
        MultiFieldPanel(
            [
                FieldPanel('activity_type', widget=forms.CheckboxSelectMultiple),  # noqa: E501
                FieldPanel('teaching_strategy', widget=forms.CheckboxSelectMultiple),  # noqa: E501
                FieldPanel('blooms_taxonomy_level', widget=forms.CheckboxSelectMultiple),  # noqa: E501
                FieldPanel('activity_duration'),
            ],
            heading="Activity characteristics",
        ),
        MultiFieldPanel(
            [
                FieldPanel('council_for_economic_education', widget=forms.CheckboxSelectMultiple),  # noqa: E501
                FieldPanel('jump_start_coalition', widget=forms.CheckboxSelectMultiple),  # noqa: E501
            ],
            heading="National standards",
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar/Footer'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    # admin use only
    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('big_idea'),
        index.SearchField('essential_questions'),
        index.SearchField('objectives'),
        index.SearchField('what_students_will_do'),
        index.FilterField('date'),
        index.FilterField('building_block'),
        index.FilterField('school_subject'),
        index.FilterField('topic'),
        index.FilterField('grade_level'),
        index.FilterField('age_range'),
        index.FilterField('student_characteristics'),
        index.FilterField('activity_type'),
        index.FilterField('teaching_strategy'),
        index.FilterField('blooms_taxonomy_level'),
        index.FilterField('activity_duration'),
        index.FilterField('jump_start_coalition'),
        index.FilterField('council_for_economic_education'),
    ]

    def get_subtopic_ids(self):
        """
        Get a list of this activity's subtopic ids
        """
        topic_ids = [topic.id for topic in self.topic.all()]
        root_ids = ActivityTopic.objects \
            .filter(id__in=topic_ids, parent=None) \
            .values_list('id', flat=True)
        return set(topic_ids) - set(root_ids)

    def get_grade_level_ids(self):
        """
        Get a list of this activity's grade_level ids
        """
        grade_level_ids = [
            grade_level.id for grade_level in self.grade_level.all()
        ]
        return grade_level_ids

    def get_related_activities_url(self):
        """
        Generate a search url for related Activities by
        subtopic and grade-level
        """
        parent_page = self.get_parent()
        subtopic_ids = [str(x) for x in self.get_subtopic_ids()]
        grade_level_ids = [str(y) for y in self.get_grade_level_ids()]

        url = parent_page.get_url() + '?q='
        if subtopic_ids:
            subtopics = '&topic=' + \
                        '&topic='.join(subtopic_ids)
            url += subtopics
        if grade_level_ids:
            grade_levels = '&grade_level=' + \
                           '&grade_level='.join(grade_level_ids)
            url += grade_levels
        return url

    def get_topics_list(self, parent=None):
        """
        Get a hierarchical list of this activity's topics.

        parent: ActivityTopic
        """
        if parent:
            descendants = set(parent.get_descendants()) & set(self.topic.all())  # noqa: E501
            children = parent.get_children()
            children_list = []
            # If this parent has descendants in self.topic, add its children.
            if descendants:
                for child in children:
                    if set(child.get_descendants()) & set(self.topic.all()):
                        children_list.append(self.get_topics_list(child))
                    elif child in self.topic.all():
                        children_list.append(child.title)

                if children_list:
                    return parent.title + " (" + ', '.join(children_list) + ")"  # noqa: E501
            # Otherwise, just add the parent.
            else:
                return parent.title
        else:
            # Build root list of topics and recurse their children.
            topic_list = []
            topic_ids = [topic.id for topic in self.topic.all()]
            ancestors = ActivityTopic.objects.filter(id__in=topic_ids).get_ancestors(True)  # noqa: E501
            roots = ActivityTopic.objects.filter(parent=None) & ancestors
            for root_topic in roots:
                topic_list.append(self.get_topics_list(root_topic))

            if topic_list:
                return ', '.join(topic_list)
            else:
                return ''

    class Meta:
        verbose_name = "TDP Activity page"


def validate_results_per_page(request):
    """
    A utility for parsing the requested number of results per page.

    This should catch an invalid number of results and always return
    a valid number of results, defaulting to 5.
    """
    raw_results = request.GET.get('results')
    if raw_results in ['10', '25', '50']:
        return int(raw_results)
    else:
        return 5


def validate_page_number(request, paginator):
    """
    A utility for parsing a pagination request.

    This should catch invalid page numbers and always return
    a valid page number, defaulting to 1.
    """
    raw_page = request.GET.get('page', 1)
    try:
        page_number = int(raw_page)
    except ValueError:
        page_number = 1
    try:
        paginator.page(page_number)
    except InvalidPage:
        page_number = 1
    return page_number
