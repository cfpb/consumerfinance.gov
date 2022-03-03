import copy
from collections import OrderedDict

from django.core.paginator import InvalidPage, Paginator
from django.db import models

from wagtail.admin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField

from elasticsearch_dsl import Q

from teachers_digital_platform.documents import ActivityPageDocument
from teachers_digital_platform.models.django import (
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
    ActivityTopic,
    ActivityType,
)
from teachers_digital_platform.models.pages import ActivityPage
from teachers_digital_platform.molecules import TdpSearchHeroImage
from v1.atomic_elements import molecules
from v1.models import CFGOVPage, CFGOVPageManager


# facet name, (facet class, is-nested)
FACET_MAP = (
    ("building_block", (ActivityBuildingBlock, False)),
    ("school_subject", (ActivitySchoolSubject, False)),
    ("topic", (ActivityTopic, True)),
    ("grade_level", (ActivityGradeLevel, False)),
    ("age_range", (ActivityAgeRange, False)),
    ("student_characteristics", (ActivityStudentCharacteristics, False)),
    ("activity_type", (ActivityType, False)),
    ("teaching_strategy", (ActivityTeachingStrategy, False)),
    ("blooms_taxonomy_level", (ActivityBloomsTaxonomyLevel, False)),
    ("activity_duration", (ActivityDuration, False)),
    ("jump_start_coalition", (ActivityJumpStartCoalition, False)),
    ("council_for_economic_education", (ActivityCouncilForEconEd, False)),
)
FACET_LIST = [tup[0] for tup in FACET_MAP]
FACET_DICT = {"aggs": {}}
for facet in FACET_LIST:
    FACET_DICT["aggs"].update(
        {"{}_terms".format(facet): {"terms": {"field": facet}}}
    )
ALWAYS_EXPANDED = {"building_block", "topic", "school_subject"}
SEARCH_FIELDS = [
    "text",
    "related_text",
    "title",
    "big_idea",
    "essential_questions",
    "objectives",
    "what_students_will_do",
]


class ActivityIndexPage(CFGOVPage):
    """A model for the Activity Search page."""

    subpage_types = ["teachers_digital_platform.ActivityPage"]

    objects = CFGOVPageManager()

    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("notification", molecules.Notification()),
        ],
        blank=True,
    )

    header_sidebar = StreamField(
        [
            ("image", TdpSearchHeroImage()),
        ],
        blank=True,
    )

    results = {}
    activity_setups = None
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("header_sidebar"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar/Footer"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super().can_create_at(parent) and not cls.objects.exists()

    def get_template(self, request):
        template = "teachers_digital_platform/activity_index_page.html"
        if "partial" in request.GET:
            template = "teachers_digital_platform/activity_search_facets_and_results.html"  # noqa: B950
        return template

    def dsl_search(self, request, *args, **kwargs):
        """Search using Elasticsearch 7 and django-elasticsearch-dsl."""
        all_facets = copy.copy(self.activity_setups.facet_setup)
        selected_facets = {}
        card_setup = self.activity_setups.ordered_cards
        total_activities = len(card_setup)
        search_query = request.GET.get("q", "")
        facet_called = any(
            [request.GET.get(facet, "") for facet in FACET_LIST]
        )
        # If there's no query or facet request, we can return cached setups:
        if not search_query and not facet_called:
            payload = {
                "search_query": search_query,
                "results": list(card_setup.values()),
                "total_results": total_activities,
                "total_activities": total_activities,
                "selected_facets": selected_facets,
                "all_facets": all_facets,
                "expanded_facets": ALWAYS_EXPANDED,
            }
            self.results = payload
            results_per_page = validate_results_per_page(request)
            paginator = Paginator(payload["results"], results_per_page)
            current_page = validate_page_number(request, paginator)
            paginated_page = paginator.page(current_page)
            context_update = {
                "facets": all_facets,
                "activities": paginated_page,
                "total_results": total_activities,
                "results_per_page": results_per_page,
                "current_page": current_page,
                "paginator": paginator,
                "show_filters": bool(selected_facets),
            }
            return context_update

        dsl_search = ActivityPageDocument().search()
        if search_query:
            terms = search_query.split()
            for term in terms:
                dsl_search = dsl_search.query(
                    "bool",
                    must=Q("multi_match", query=term, fields=SEARCH_FIELDS),
                )
        else:
            dsl_search = dsl_search.sort("-date")
        for facet, _ in FACET_MAP:
            if facet in request.GET and request.GET.get(facet):
                facet_ids = [
                    value
                    for value in request.GET.getlist(facet)
                    if value.isdigit()
                ]
                selected_facets[facet] = facet_ids
        for facet, pks in selected_facets.items():
            dsl_search = dsl_search.query(
                "bool", should=[Q("match", **{facet: pk}) for pk in pks]
            )
        facet_search = dsl_search.update_from_dict(FACET_DICT)
        total_results = dsl_search.count()
        dsl_search = dsl_search[:total_results]
        response = dsl_search.execute()
        results = [card_setup[str(hit.id)] for hit in response[:total_results]]
        facet_response = facet_search.execute()
        facet_counts = {
            facet: getattr(
                facet_response.aggregations, f"{facet}_terms"
            ).buckets
            for facet in FACET_LIST
        }
        all_facets = parse_dsl_facets(
            all_facets, facet_counts, selected_facets
        )
        payload = {
            "search_query": search_query,
            "results": results,
            "total_results": total_results,
            "total_activities": total_activities,
            "selected_facets": selected_facets,
            "all_facets": all_facets,
        }
        # List all facet blocks that need to be expanded
        conditionally_expanded = {
            facet_name
            for facet_name, facet_items in all_facets.items()
            if any(facet["selected"] is True for facet in facet_items)
        }
        expanded_facets = ALWAYS_EXPANDED.union(set(conditionally_expanded))
        payload.update(
            {
                "expanded_facets": expanded_facets,
            }
        )
        self.results = payload
        results_per_page = validate_results_per_page(request)
        paginator = Paginator(payload["results"], results_per_page)
        current_page = validate_page_number(request, paginator)
        paginated_page = paginator.page(current_page)
        context_update = {
            "facets": all_facets,
            "activities": paginated_page,
            "total_results": total_results,
            "results_per_page": results_per_page,
            "current_page": current_page,
            "paginator": paginator,
            "show_filters": bool(selected_facets),
        }
        return context_update

    def get_context(self, request, *args, **kwargs):
        if not self.activity_setups:
            self.activity_setups = get_activity_setup()
        context_update = self.dsl_search(request, *args, **kwargs)
        context = super().get_context(request)
        context.update(context_update)
        return context

    class Meta:
        verbose_name = "TDP Activity search page"


def parse_dsl_facets(all_facets, facet_counts, selected_facets):
    for facet, facet_config in FACET_MAP:
        returned_facet_ids = [hit["key"] for hit in facet_counts[facet]]
        is_nested = facet_config[1]
        selections = selected_facets.get(facet, "")
        if is_nested:
            for pi, parent in enumerate(all_facets[facet]):
                if parent["id"] in selections:
                    parent["selected"] = True
                    parent["child_selected"] = True
                    for _, child in enumerate(parent["children"]):
                        child["selected"] = True
                else:
                    for _, child in enumerate(parent["children"]):
                        if selections and child["id"] in selections:
                            child["selected"] = True
                            parent["child_selected"] = True
                all_facets[facet][pi].update(parent)
            for pi, parent in enumerate(all_facets[facet]):
                for child in parent["children"]:
                    if child["id"] not in returned_facet_ids:
                        parent["children"].remove(child)
                all_facets[facet][pi].update(parent)
            for parent in all_facets[facet]:
                if not parent["children"]:
                    all_facets[facet].remove(parent)
        else:
            for i, flat_facet in enumerate(all_facets[facet]):
                flat_id = flat_facet["id"]
                if selections and flat_id in selections:
                    flat_facet["selected"] = True
                    all_facets[facet][i].update(flat_facet)
            for flat_facet in all_facets[facet]:
                flat_id = flat_facet["id"]
                if (
                    flat_id not in returned_facet_ids
                    and flat_id not in selections
                ):
                    all_facets[facet].remove(flat_facet)
    return all_facets


def default_nested_facets(class_object):
    """Build a nested facet tree, initially only for ActivityTopic objects."""
    setup = []
    parents = class_object.objects.filter(parent=None)
    default_attrs = {
        "selected": False,
        "child_selected": False,
        "children": None,
        "parent": None,
    }
    for parent in parents:
        parent_setup = copy.copy(default_attrs)
        parent_setup.update({"id": str(parent.id), "title": parent.title})
        child_setups = []
        for child in parent.children.exclude(activitypage=None):
            _child_setup = copy.copy(default_attrs)
            _child_setup.update(
                {
                    "id": str(child.id),
                    "title": child.title,
                    "parent": str(child.parent_id),
                }
            )
            child_setups.append(_child_setup)
        parent_setup["children"] = child_setups
        setup.append(parent_setup)
    return setup


def default_flat_facets(class_object):
    return [
        {"selected": False, "id": str(obj.id), "title": obj.title}
        for obj in class_object.objects.all()
    ]


class ActivitySetUp(models.Model):
    """A database cache of form setups for TDP activities."""

    card_setup = models.JSONField(blank=True, null=True)
    card_order = models.JSONField(blank=True, null=True)
    facet_setup = models.JSONField(blank=True, null=True)

    def __str__(self):
        return "Cached activity facets and cards"

    def update_facets(self):
        _facet_setup = {}
        for facet_name, facet_config in FACET_MAP:
            class_object, is_nested = facet_config
            if is_nested:
                _facet_setup[facet_name] = default_nested_facets(class_object)
            else:
                _facet_setup[facet_name] = default_flat_facets(class_object)
        self.facet_setup = _facet_setup

    def update_cards(self):
        _card_setup = {}
        # The information needed for displaying each result of a query
        facet_fields = (
            "school_subject",
            "grade_level",
            "age_range",
            "student_characteristics",
            "activity_type",
            "teaching_strategy",
            "blooms_taxonomy_level",
            "jump_start_coalition",
            "council_for_economic_education",
        )
        base_query = ActivityPage.objects.filter(live=True).order_by(
            "-date", "title"
        )
        self.card_order = [a.pk for a in base_query]
        for activity in base_query:
            payload = {
                "url": activity.url,
                "title": activity.title,
                "date": activity.date.strftime("%b %d, %Y"),
                "date_attr": activity.date.strftime("%Y-%m-%d"),
                "ideal_for": ", ".join(
                    [gl.title for gl in activity.grade_level.all()]
                ),
                "summary": activity.summary,
                "topic": activity.get_topics_list(),
                "activity_duration": activity.activity_duration.title,
                "available_in_spanish": activity.activity_type.filter(
                    title="Available in Spanish"
                ).exists(),
                "building_block": [
                    {"title": blk.title, "svg_icon": blk.svg_icon}
                    for blk in activity.building_block.all()
                ],
            }
            for field in facet_fields:
                facet_queryset = getattr(activity, field).all()
                payload.update({field: [obj.title for obj in facet_queryset]})
            _card_setup.update({str(activity.pk): payload})
        self.card_setup = _card_setup

    @property
    def ordered_cards(self):
        return OrderedDict(
            {str(pk): self.card_setup[str(pk)] for pk in self.card_order}
        )

    def update_setups(self):
        self.update_facets()
        self.update_cards()
        self.save()


def get_activity_setup(refresh=False):
    if not ActivitySetUp.objects.exists():
        ActivitySetUp().update_setups()
        return ActivitySetUp.objects.first()
    map_obj = ActivitySetUp.objects.first()
    if refresh:
        map_obj.update_setups()
        map_obj.refresh_from_db()
    return map_obj


def validate_results_per_page(request):
    """
    A utility for parsing the requested number of results per page.

    This should catch an invalid number of results and always return
    a valid number of results, defaulting to 5.
    """
    raw_results = request.GET.get("results")
    if raw_results in ["10", "25", "50"]:
        return int(raw_results)
    else:
        return 5


def validate_page_number(request, paginator):
    """
    A utility for parsing a pagination request.

    This should catch invalid page numbers and always return
    a valid page number, defaulting to 1.
    """
    raw_page = request.GET.get("page", 1)
    try:
        page_number = int(raw_page)
    except ValueError:
        page_number = 1
    try:
        paginator.page(page_number)
    except InvalidPage:
        page_number = 1
    return page_number
