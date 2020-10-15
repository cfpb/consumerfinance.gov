from django.contrib.postgres.fields import JSONField
from django.core.paginator import InvalidPage, Paginator
from django.db import models
from haystack.query import SearchQuerySet

from wagtail.admin.edit_handlers import (
    ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core.fields import StreamField

from flags.state import flag_enabled

from teachers_digital_platform.models.django import (
    ActivityAgeRange, ActivityBloomsTaxonomyLevel, ActivityBuildingBlock,
    ActivityCouncilForEconEd, ActivityDuration, ActivityGradeLevel,
    ActivityJumpStartCoalition, ActivitySchoolSubject,
    ActivityStudentCharacteristics, ActivityTeachingStrategy, ActivityTopic,
    ActivityType
)

from teachers_digital_platform.documents import ActivityPageDocument
from teachers_digital_platform.molecules import TdpSearchHeroImage
from teachers_digital_platform.models.pages import ActivityPage
from v1.atomic_elements import molecules
from v1.models import CFGOVPage, CFGOVPageManager

from elasticsearch_dsl import FacetedSearch, TermsFacet

FACET_MAP = (
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
FACET_LIST = [tup[0] for tup in FACET_MAP]


class FacetSearch(FacetedSearch):
    index = 'teachers-digital-platform'
    doc_types = FACET_LIST
    fields = ['pk']
    facets = {doc: TermsFacet(field='pk') for doc in doc_types}


class ActivityIndexPage(CFGOVPage):
    """A model for the Activity Search page."""

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

    def dsl_search(self, request, *args, **kwargs):
        activity_card_map = get_activity_card_map()
        total_activities = len(activity_card_map)
        search_query = request.GET.get('q', '')
        doc_search = ActivityPageDocument.search()
        all_facet_search = FacetSearch(",".join(FACET_LIST))
        search = doc_search.query(
            'match', _all=search_query)

        # Load selected facets
        selected_facets = {}
        facet_queries = {}
        for facet, facet_config in FACET_MAP:
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
            search = search.filter(
                content=search_query)  # .order_by('-_score', '-date')
        else:
            search = search  # .order_by('-date')

        # Get all facets and their counts
        facet_counts = all_facet_search.facet_counts()
        all_facets = self.get_all_facets(
            FACET_MAP,
            all_facet_search,
            facet_counts,
            facet_queries,
            selected_facets,
        )

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
            search = search.narrow(facet_narrow_query)

        results = [activity_card_map[activity.pk] for activity in search]
        total_results = len(results)

        payload.update({
            'results': results,
            'total_results': total_results,
        })
        self.results = payload
        results_per_page = validate_results_per_page(request)
        paginator = Paginator(payload['results'], results_per_page)
        current_page = validate_page_number(request, paginator)
        paginated_page = paginator.page(current_page)
        context_update = {
            'facet_counts': facet_counts,
            'facets': all_facets,
            'activities': paginated_page,
            'total_results': total_results,
            'results_per_page': results_per_page,
            'current_page': current_page,
            'paginator': paginator,
            'show_filters': bool(facet_queries),
        }
        return context_update

    def haystack_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '')  # haystack cleans this string
        sqs = SearchQuerySet().models(ActivityPage)
        total_activities = sqs.count()
        # Load selected facets
        selected_facets = {}
        facet_queries = {}
        activity_card_map = get_activity_card_map()

        for facet, facet_config in FACET_MAP:
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
            sqs = sqs.filter(
                content=search_query).order_by('-_score', '-date')
        else:
            sqs = sqs.order_by('-date')

        # Get all facets and their counts
        facet_counts = sqs.facet_counts()
        all_facets = self.get_all_facets(
            FACET_MAP, sqs, facet_counts, facet_queries, selected_facets
        )

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

        results = [activity_card_map[activity.pk] for activity in sqs]
        total_results = len(results)

        payload.update({
            'results': results,
            'total_results': total_results,
        })
        self.results = payload
        results_per_page = validate_results_per_page(request)
        paginator = Paginator(payload['results'], results_per_page)
        current_page = validate_page_number(request, paginator)
        paginated_page = paginator.page(current_page)

        context_update = {
            'facet_counts': facet_counts,
            'facets': all_facets,
            'activities': paginated_page,
            'total_results': total_results,
            'results_per_page': results_per_page,
            'current_page': current_page,
            'paginator': paginator,
            'show_filters': bool(facet_queries),
        }
        return context_update

    def get_context(self, request, *args, **kwargs):
        if flag_enabled('ELASTICSEARCH_DSL_TDP'):
            context_update = self.dsl_search(request, *args, **kwargs)
        else:
            context_update = self.haystack_search(request, *args, **kwargs)
        context = super(ActivityIndexPage, self).get_context(request)
        context.update(context_update)
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


class ActivityCardMap(models.Model):
    card_map = JSONField(blank=True, null=True)

    def __str__(self):
        return "Cached Activity Page cards"

    def update_cards(self):
        facet_fields = (
            'school_subject',
            'grade_level',
            'age_range',
            'student_characteristics',
            'activity_type',
            'teaching_strategy',
            'blooms_taxonomy_level',
            'jump_start_coalition',
            'council_for_economic_education',
        )
        _card_map = {}
        base_query = ActivityPage.objects.filter(live=True)
        for activity in base_query:
            payload = {
                'url': activity.url,
                'title': activity.title,
                'date': activity.date.strftime("%b %d, %Y"),
                'date_attr': activity.date.strftime("%Y-%m-%d"),
                'ideal_for': ", ".join([
                    gl.title for gl in activity.grade_level.all()
                ]),
                'summary': activity.summary,
                'topic': activity.get_topics_list(),
                'activity_duration': activity.activity_duration.title,
                'building_block': [
                    {'title': blk.title, 'svg_icon': blk.svg_icon}
                    for blk in activity.building_block.all()
                ]
            }
            for field in facet_fields:
                facet_queryset = getattr(activity, field).all()
                payload.update({
                    field: [obj.title for obj in facet_queryset]
                })
            _card_map[activity.pk] = payload
        self.card_map = _card_map
        self.save()


def get_activity_card_map():
    if not ActivityCardMap.objects.first():
        ActivityCardMap().update_cards()
    return ActivityCardMap.objects.first().card_map


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
