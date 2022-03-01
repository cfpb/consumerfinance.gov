import logging
import re
import urllib
from collections import OrderedDict
from datetime import date
from functools import partial
from urllib.parse import urljoin

from django.core.exceptions import ValidationError
from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template.response import TemplateResponse

from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtailsharing.models import ShareableRoutablePageMixin

import requests
from jinja2 import Markup
from regdown import regdown

from ask_cfpb.models.pages import SecondaryNavigationJSMixin
from regulations3k.blocks import RegulationsListingFullWidthText
from regulations3k.documents import SectionParagraphDocument
from regulations3k.forms import SearchForm
from regulations3k.models import Part, Section, label_re_str
from regulations3k.resolver import get_contents_resolver, get_url_resolver
from v1.atomic_elements import molecules, organisms
from v1.models import CFGOVPage, CFGOVPageManager


logger = logging.getLogger(__name__)


class RegulationsSearchPage(RoutablePageMixin, CFGOVPage):
    """A page for the custom search interface for regulations."""

    objects = PageManager()

    parent_page_types = ["regulations3k.RegulationLandingPage"]
    subpage_types = []
    results = {}
    content_panels = CFGOVPage.content_panels
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    def get_template(self, request):
        template = "regulations3k/search-regulations.html"
        if "partial" in request.GET:
            template = "regulations3k/search-regulations-results.html"
        return template

    @route(r"^results/")
    def regulation_results_page(self, request):
        all_regs = Part.objects.order_by("part_number")
        regs = validate_regs_list(request)
        order = validate_order(request)

        payload = {
            "search_query": "",
            "results": [],
            "total_results": 0,
            "regs": regs,
            "all_regs": [],
        }

        search_form = SearchForm(request.GET)
        if (
            not search_form.is_valid()
            or len(urllib.parse.unquote(search_form.cleaned_data["q"])) == 1
        ):
            self.results = payload
            return TemplateResponse(
                request, self.get_template(request), self.get_context(request)
            )

        search_query = search_form.cleaned_data["q"]
        payload["search_query"] = search_query

        search = SectionParagraphDocument.search().query(
            "match", text={"query": search_query, "operator": "AND"}
        )
        search = search.highlight("text", pre_tags="<strong>", post_tags="</strong>")
        total_results = search.count()
        all_regs = [
            {
                "short_name": reg.short_name,
                "id": reg.part_number,
                "num_results": search.filter("term", part=reg.part_number).count(),
                "selected": reg.part_number in regs,
            }
            for reg in all_regs
        ]
        payload.update({"all_regs": all_regs, "total_count": total_results})
        if regs:
            search = search.filter("terms", part=regs)
        if order == "regulation":
            search = search.sort("part", "section_order")
        search = search[0:total_results]
        response = search.execute()
        for hit in response[0:total_results]:
            try:
                snippet = Markup("".join(hit.meta.highlight.text[0]))
            except TypeError as e:
                logger.warning(
                    "Query string {} produced a TypeError: {}".format(search_query, e)
                )
                continue
            hit_payload = {
                "id": hit.paragraph_id,
                "part": hit.part,
                "reg": hit.short_name,
                "label": hit.title,
                "snippet": snippet,
                "url": "{}{}/{}/#{}".format(
                    self.parent().url,
                    hit.part,
                    hit.section_label.lower(),
                    hit.paragraph_id,
                ),
            }
            payload["results"].append(hit_payload)

        payload.update({"current_count": search.count()})
        self.results = payload
        context = self.get_context(request)
        num_results = validate_num_results(request)
        paginator = Paginator(payload["results"], num_results)
        page_number = validate_page_number(request, paginator)
        paginated_page = paginator.page(page_number)
        context.update(
            {
                "current_count": payload["current_count"],
                "total_count": payload["total_count"],
                "paginator": paginator,
                "current_page": page_number,
                "num_results": num_results,
                "order": order,
                "results": paginated_page,
                "show_filters": any(
                    reg["selected"] is True for reg in payload["all_regs"]
                ),
            }
        )
        return TemplateResponse(request, self.get_template(request), context)


class RegulationLandingPage(ShareableRoutablePageMixin, CFGOVPage):
    """Landing page for eregs."""

    header = StreamField(
        [
            ("hero", molecules.Hero()),
        ],
        blank=True,
    )
    content = StreamField(
        [
            ("notification", molecules.Notification()),
            ("full_width_text", RegulationsListingFullWidthText()),
        ],
        blank=True,
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    objects = CFGOVPageManager()
    subpage_types = ["regulations3k.RegulationPage", "RegulationsSearchPage"]
    template = "regulations3k/landing-page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "get_secondary_nav_items": get_secondary_nav_items,
            }
        )
        return context

    @route(r"^recent-notices-json/$", name="recent_notices")
    def recent_notices(self, request):
        fr_api_url = "https://www.federalregister.gov/api/v1/"
        fr_documents_url = fr_api_url + "documents.json"
        params = {
            "fields_list": ["html_url", "title"],
            "per_page": "3",
            "order": "newest",
            "conditions[agencies][]": "consumer-financial-protection-bureau",
            "conditions[type][]": "RULE",
            "conditions[cfr][title]": "12",
        }
        response = requests.get(fr_documents_url, params=params)

        if response.status_code != 200:
            return HttpResponse(status=response.status_code)

        return JsonResponse(response.json())


class RegulationPage(ShareableRoutablePageMixin, SecondaryNavigationJSMixin, CFGOVPage):
    """A routable page for serving an eregulations page by Section ID."""

    objects = PageManager()
    parent_page_types = ["regulations3k.RegulationLandingPage"]
    subpage_types = []

    template = "regulations3k/browse-regulation.html"

    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
        ],
        blank=True,
    )

    content = StreamField(
        [
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("full_width_text", organisms.FullWidthText()),
        ],
        null=True,
        blank=True,
    )

    regulation = models.ForeignKey(
        Part,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="page",
    )

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
        FieldPanel("regulation", Part),
    ]

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel("secondary_nav_exclude_sibling_pages"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(sidefoot_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    def can_serve_draft_versions(self, request):
        perms = request.user.get_all_permissions()
        if (
            request.user.is_superuser
            or getattr(request, "served_by_wagtail_sharing", False)
            or "regulations3k.change_section" in perms
        ):
            return True
        return False

    def get_versions_query(self, request):
        versions = self.regulation.versions

        if not self.can_serve_draft_versions(request):
            versions = versions.filter(draft=False)

        return versions

    def get_effective_version(self, request, date_str=None):
        """Get the requested effective version if the user has permission"""
        query_filter = {}

        if date_str is None:
            query_filter["effective_date__lte"] = date.today()
        else:
            query_filter["effective_date"] = date_str

        draft_permission = self.can_serve_draft_versions(request)
        if not draft_permission:
            query_filter["draft"] = False

        try:
            effective_version = (
                self.regulation.versions.filter(**query_filter)
                .order_by("-effective_date")
                .first()
            )
        except ValidationError:
            # This can be raised by an invalid date string
            raise Http404

        if effective_version is None:
            raise Http404

        return effective_version

    def get_section_query(self, request=None, effective_version=None):
        """Query set for Sections in this regulation's effective version."""
        if effective_version is None:
            effective_version = self.get_effective_version(request)
        return Section.objects.filter(subpart__version=effective_version)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "regulation": self.regulation,
                "current_version": self.get_effective_version(request),
                "breadcrumb_items": self.get_breadcrumbs(request, *args, **kwargs),
                "search_url": (
                    self.get_parent().url
                    + "search-regulations/results/?regs="
                    + self.regulation.part_number
                ),
                "num_versions": self.get_versions_query(request).count(),
            }
        )
        return context

    def get_breadcrumbs(self, request, section=None, **kwargs):
        crumbs = super().get_breadcrumbs(request)

        if section is not None:
            crumbs = crumbs + [
                {
                    "href": self.url
                    + self.reverse_subpage(
                        "index",
                        kwargs={k: v for k, v in kwargs.items() if k == "date_str"},
                    ),
                    "title": str(section.subpart.version.part),
                },
            ]

        return crumbs

    def get_urls_for_version(self, effective_version, section=None):
        base_url = self.get_full_url()
        versions_url = urljoin(base_url, "versions") + "/"

        if effective_version.live_version:
            # This is the current version
            version_url = base_url
        else:
            # It's a past or future version, URLs have the date str
            date_str = str(effective_version.effective_date)
            version_url = urljoin(base_url, date_str) + "/"
            yield version_url

        if section is not None:
            yield urljoin(version_url, section.label) + "/"
        else:
            sections = self.get_section_query(effective_version=effective_version)
            yield version_url
            yield versions_url
            for section in sections.all():
                yield urljoin(version_url, section.label) + "/"

    def render_interp(self, context, raw_contents, **kwargs):
        template = get_template("regulations3k/inline_interps.html")

        # Extract the title from the raw regdown
        section_title_match = re.search(r"#+\s?(?P<section_title>.*)\s", raw_contents)
        if section_title_match is not None:
            context.update({"section_title": section_title_match.group(1)})
            span = section_title_match.span()
            raw_contents = raw_contents[: span[0]] + raw_contents[span[1] :]

        context.update({"contents": regdown(raw_contents)})
        context.update(kwargs)

        return template.render(context)

    @route(r"^(?:(?P<date_str>[0-9]{4}-[0-9]{2}-[0-9]{2})/)?$", name="index")
    def index_route(self, request, date_str=None):
        request.is_preview = getattr(request, "is_preview", False)

        effective_version = self.get_effective_version(request, date_str=date_str)
        section_query = self.get_section_query(effective_version=effective_version)
        sections = list(section_query.all())

        context = self.get_context(request)
        context.update(
            {
                "requested_version": effective_version,
                "sections": sections,
                "get_secondary_nav_items": partial(
                    get_secondary_nav_items,
                    sections=sections,
                    date_str=date_str,
                ),
            }
        )

        if date_str is not None:
            context["date_str"] = date_str

        return TemplateResponse(request, self.get_template(request), context)

    @route(
        r"^versions/(?:(?P<section_label>" + label_re_str + r")/)?$",
        name="versions",
    )
    def versions_page(self, request, section_label=None):
        section_query = self.get_section_query(request=request)
        sections = list(section_query.all())
        context = self.get_context(request, sections=sections)

        versions = [
            {
                "effective_date": v.effective_date,
                "date_str": str(v.effective_date),
                "sections": self.get_section_query(effective_version=v).all(),
                "draft": v.draft,
            }
            for v in self.get_versions_query(request).order_by("-effective_date")
        ]

        context.update(
            {
                "versions": versions,
                "section_label": section_label,
                "get_secondary_nav_items": partial(
                    get_secondary_nav_items, sections=sections
                ),
            }
        )

        return TemplateResponse(request, self.template, context)

    @route(
        r"^(?:(?P<date_str>[0-9]{4}-[0-9]{2}-[0-9]{2})/)?"
        r"(?P<section_label>" + label_re_str + r")/$",
        name="section",
    )
    def section_page(self, request, date_str=None, section_label=None):
        """Render a section of the currently effective regulation"""

        effective_version = self.get_effective_version(request, date_str=date_str)
        section_query = self.get_section_query(effective_version=effective_version)

        next_version = (
            self.get_versions_query(request)
            .filter(effective_date__gt=effective_version.effective_date)
            .first()
        )

        kwargs = {}
        if date_str is not None:
            kwargs["date_str"] = date_str

        try:
            section = section_query.get(label__iexact=section_label)
            if re.search("[A-Z]+", section_label):
                return redirect(
                    self.url
                    + self.reverse_subpage("index", kwargs=kwargs)
                    + section.url_path
                    + "/",
                    permanent=True,
                )
        except Section.DoesNotExist:
            return redirect(self.url + self.reverse_subpage("index", kwargs=kwargs))

        sections = list(section_query.all())
        current_index = sections.index(section)
        context = self.get_context(request, section, sections=sections, **kwargs)

        content = regdown(
            section.contents,
            url_resolver=get_url_resolver(self, date_str=date_str),
            contents_resolver=get_contents_resolver(effective_version),
            render_block_reference=partial(self.render_interp, context),
        )

        next_section = get_next_section(sections, current_index)
        previous_section = get_previous_section(sections, current_index)

        context.update(
            {
                "requested_version": effective_version,
                "next_version": next_version,
                "section": section,
                "content": content,
                "get_secondary_nav_items": partial(
                    get_secondary_nav_items,
                    sections=sections,
                    date_str=date_str,
                ),
                "next_section": next_section,
                "next_url": get_section_url(self, next_section, date_str=date_str),
                "previous_section": previous_section,
                "previous_url": get_section_url(
                    self, previous_section, date_str=date_str
                ),
            }
        )

        return TemplateResponse(request, self.template, context)


def get_next_section(section_list, current_index):
    if current_index == len(section_list) - 1:
        return None
    else:
        return section_list[current_index + 1]


def get_previous_section(section_list, current_index):
    if current_index == 0:
        return None
    else:
        return section_list[current_index - 1]


def get_section_url(page, section, date_str=None):
    if section is None:
        return None

    section_kwargs = {}
    if date_str is not None:
        section_kwargs["date_str"] = date_str

    section_kwargs["section_label"] = section.label
    return (page.url + page.reverse_subpage("section", kwargs=section_kwargs)).lower()


def get_secondary_nav_items(request, current_page, sections=[], date_str=None):
    url_bits = [bit for bit in request.path.split("/") if bit]
    current_label = url_bits[-1]
    subpart_dict = OrderedDict()

    section_kwargs = {}
    if date_str is not None:
        section_kwargs["date_str"] = date_str

    for section in sections:
        # If the section's subpart isn't in the subpart dict yet, add it
        if section.subpart not in subpart_dict:
            subpart_dict[section.subpart] = {"sections": [], "expanded": False}

        section_kwargs["section_label"] = section.label

        # Create the section dictionary for navigation
        section_dict = {
            "title": section.title,
            "url": get_section_url(current_page, section, date_str=date_str),
            "active": section.url_path == current_label,
            "expanded": True,
            "section": section,
        }

        # Add it to the subpart
        subpart_dict[section.subpart]["sections"].append(section_dict)

        # Set the subpart to active if the section is active
        if section_dict["active"]:
            subpart_dict[section.subpart]["expanded"] = True

    return subpart_dict, False


def validate_num_results(request):
    """
    A utility for parsing the requested number of results per page.

    This should catch an invalid number of results and always return
    a valid number of results, defaulting to 25.
    """
    raw_results = request.GET.get("results")
    if raw_results in ["50", "100"]:
        return int(raw_results)
    else:
        return 25


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


def validate_regs_list(request):
    """
    A utility for validating a RegulationsSearchPage request.

    Validates that a list of regulation part numbers is alphanumeric.
    """
    if "regs" in request.GET and request.GET.get("regs"):
        regs_input_list = request.GET.getlist("regs")
        return [reg for reg in regs_input_list if reg.isalnum()]
    else:
        return []


def validate_order(request):
    order = request.GET.get("order")
    if order not in ("relevance", "regulation"):
        order = "relevance"
    return order
