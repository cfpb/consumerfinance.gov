import datetime
import logging

import requests
from dateutil import parser

from regulations3k.models import EffectiveVersion, Part
from regulations3k.parser.patterns import title_pattern


CFR_TITLE = "12"
CFR_CHAPTER = "X"
FR_date_query = (
    "https://www.federalregister.gov/api/v1/documents.json?"
    "fields[]=effective_on&"
    "per_page=20&"
    "order=relevance&"
    "conditions[agencies][]=consumer-financial-protection-bureau&"
    "conditions[type][]=RULE&"
    "conditions[cfr][title]=12&"
    "conditions[cfr][part]={}"
)
logger = logging.getLogger(__name__)


class PayLoad:
    """Stash regulation components and interp references as they are built."""

    def __init__(self):
        self.part = None
        self.effective_date = None
        self.version = None
        self.subparts = {
            "section_subparts": [],
            "appendix_subpart": None,
            "interp_subpart": None,
        }
        self.sections = []
        self.appendices = []
        self.interpretations = []
        self.tables = {}
        self.interp_refs = {}

    def reset(self):
        self.interp_refs = {}
        self.tables = {}
        for element in [
            self.effective_date,
            self.part,
            self.version,
            self.subparts["appendix_subpart"],
            self.subparts["interp_subpart"],
        ]:
            element = None  # noqa: F841
        for list_element in [
            self.subparts["section_subparts"],
            self.sections,
            self.appendices,
            self.interpretations,
        ]:
            list_element = []  # noqa: F841

    def get_effective_date(self, part_number):
        today = datetime.date.today()
        FR_query = FR_date_query.format(part_number)
        FR_response = requests.get(FR_query)
        if not FR_response.ok or not FR_response.json():
            return
        FR_json = FR_response.json()
        date_strings = [
            result["effective_on"] for result in FR_json["results"]
        ]
        dates = sorted(
            set([parser.parse(date).date() for date in date_strings if date])
        )
        self.effective_date = [date for date in dates if date <= today][-1]

    def parse_part(self, part_soup, part_number):
        part, created = Part.objects.get_or_create(
            part_number=part_number,
            chapter=CFR_CHAPTER,
            cfr_title_number=CFR_TITLE,
        )
        if created:
            raw_title = part_soup.find("HEAD").text
            parsed_title = title_pattern.match(raw_title)
            part.title = parsed_title.group(2).title()
            part.short_name = (
                parsed_title.group(3).replace("REGULATION", "").strip()
            )
            part.save()
        self.part = part

    def parse_version(self, soup, part):
        auth = soup.find("AUTH").find("PSPACE").text.strip()
        source = soup.find("SOURCE").find("PSPACE").text.strip()
        version = EffectiveVersion(
            created=datetime.date.today(),
            effective_date=self.effective_date,
            authority=auth,
            part=part,
            source=source,
            draft=True,
        )
        version.save()
        self.version = version
