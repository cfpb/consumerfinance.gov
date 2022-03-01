import re

from django.shortcuts import redirect

from dateutil import parser

from regulations3k.forms import SearchForm
from regulations3k.models import EffectiveVersion


# Mapping of document number to effective date
VERSION_MAP = {
    "1002": {
        "2017-20417_20220101": "2022-01-01",
        # '2017-20417_20180101': '2018-01-01',  # current regulation
        "2016-16301": "2016-07-11",
        "2013-22752_20140110": "2014-01-10",
        "2013-22752_20140101": "2014-01-01",
        "2011-31714": "2011-12-30",
    },
    "1003": {
        "2015-26607_20200101": "2020-01-01",
        "2015-26607_20190101": "2019-01-01",
        # '2017-18284_20180101': '2018-01-01',  # current regulation
        "2015-26607_20170101": "2017-01-01",
        "2016-30731": "2016-01-01",
        "2014-30404": "2015-01-01",
        "2013-31223": "2014-01-01",
        "2012-31311": "2012-12-31",
        "2012-3460": "2012-02-15",
        "2011-31712": "2011-12-30",
    },
    "1004": {
        # '2011-18676': '2011-07-22',  # current regulation
    },
    "1005": {
        "2018-01305": "2019-01-01",
        # '2016-24506': '2016-11-14',  # current regulation
        "2014-20681": "2014-11-17",
        "2013-19503": "2013-10-28",
        "2013-06861": "2013-03-26",
        "2011-31725": "2011-12-30",
    },
    "1010": {
        # '2016-10715': '2016-06-10',  # current regulation
        "2011-31713": "2011-12-30",
    },
    "1011": {
        # '2011-31713': '2011-12-30',  # current regulation
    },
    "1012": {
        # '2012-10602': '2012-05-03',  # current regulation
        "2011-31713": "2011-12-30",
    },
    "1013": {
        # '2017-24411': '2018-01-01',  # current regulation
        "2016-28710": "2017-01-01",
        "2015-30071": "2016-01-01",
        "2014-21847": "2015-01-01",
        "2013-28194": "2014-01-01",
        "2012-27996": "2013-01-01",
        "2011-31723": "2011-12-30",
    },
    "1024": {
        # '2017-21912': '2017-10-19',  # current regulation
        "2015-18239": "2015-10-03",
        "2013-15466": "2014-02-14",
        "2013-24521": "2014-01-10",
        "2013-09750": "2013-06-03",
        "2011-31722": "2011-12-30",
    },
    "1026": {
        "2018-01305": "2019-04-01",
        # '2018-09243': '2018-06-01',  # current regulation
        "2018-04823": "2018-04-19",
        "2017-24445": "2018-01-01",
        "2017-15764": "2017-10-10",
        "2016-24503": "2017-10-01",
        "2016-30730": "2017-01-01",
        "2016-14782_20160627": "2016-06-27",
        "2016-06834": "2016-03-31",
        "2015-32293": "2016-01-01",
        "2015-32463": "2015-12-24",
        "2015-18239": "2015-10-03",
        "2015-12719": "2015-08-10",
        "2013-30108_20150718": "2015-07-18",
        "2015-09000": "2015-04-17",
        "2014-30419": "2015-01-01",
        "2013-30108_20140118": "2014-01-18",
        "2013-24521": "2014-01-10",
        "2013-31225": "2014-01-01",
        "2013-16962_20130724": "2013-07-24",
        "2013-12125": "2013-06-01",
        "2013-10429": "2013-05-03",
        "2013-07066": "2013-03-28",
        "2012-27997": "2013-01-01",
        "2012-28341": "2012-11-23",
        "2011-31715": "2011-12-30",
    },
    "1030": {
        # '2011-31727': '2011-12-30',  # current regulation
    },
}
INTERP_APPENDIX_DEFAULTS = {"1024": "MS", "1002": "C"}
INTERP_SECTION_DEFAULTS = {
    "1003": "2",
    "1005": "2",
    "1024": "5",
}
SEARCH_RE = re.compile(r"/eregulations/search/(\d{4})")
SECTION_RE = re.compile(r"/eregulations/\d{4}-(\d{1,3})/([0-9_-]+)")
APPENDIX_RE = re.compile(r"/eregulations/\d{4}-([A-Z1-2]{1,3})/([0-9_-]+)")
INTERP_INTRO_RE = re.compile(r"/eregulations/\d{4}-Interp-h1/([0-9_-]+)", re.IGNORECASE)
INTERP_APPENDIX_RE = re.compile(
    r"/eregulations/\d{4}-Appendices-Interp/([0-9_-]+)", re.IGNORECASE
)
INTERP_SECTION_RE = re.compile(
    r"/eregulations/(?:\d{4}-)(?:Subpart-)?(?:[A-Z-]+)?Interp(?:-[A-Z0-9]{1,2})?/([0-9_-]+)",
    re.IGNORECASE,
)  # noqa


def get_version_date(part_number, doc_number):
    """Return a version date string if there's a valid associated version."""
    if doc_number not in VERSION_MAP[part_number]:
        return
    version_date = VERSION_MAP[part_number][doc_number]
    effective_date = parser.parse(version_date).date()
    if EffectiveVersion.objects.filter(
        part__part_number=part_number,
        effective_date=effective_date,
        draft=False,
    ).exists():
        return version_date


def redirect_eregs(request, **kwargs):
    """
    Redirect legacy eregulations pages to the relevant regulations3k page.

    If a regulation version doesn't exist in regs3k or isn't approved yet,
    requests for that version will be redirected to the current regulation
    version in regulations3k.
    """
    original_url = request.path
    original_base = "/eregulations/"
    new_base = "/policy-compliance/rulemaking/regulations/"
    if original_url == original_base:
        return redirect(new_base, permanent=True)
    search_base = SEARCH_RE.match(original_url)
    if search_base:
        part = search_base.group(1)
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data["q"]
        else:
            query = ""
        return redirect(
            f"{new_base}search-regulations/results/?regs={part}&q={query}",
            permanent=True,
        )
    part_match = re.match(r"/eregulations/(\d{4})", original_url)
    if not part_match:
        return redirect(new_base)
    if part_match.group(1) in VERSION_MAP:
        part = part_match.group(1)
    else:
        return redirect(new_base, permanent=True)
    if original_url == f"{original_base}{part}":
        return redirect(f"{new_base}{part}/", permanent=True)
    for pattern in [SECTION_RE, APPENDIX_RE]:
        match_base = pattern.match(original_url)
        if match_base:
            (section, doc) = (match_base.group(1), match_base.group(2))
            # permanently redirect current or unknown versions
            if doc not in VERSION_MAP[part]:
                return redirect(f"{new_base}{part}/{section}/", permanent=True)
            version_date = get_version_date(part, doc)
            # if known version is not ready, temp redirect to current
            if not version_date:
                return redirect(f"{new_base}{part}/{section}/")
            # permanently redirect known, ready versions
            return redirect(
                f"{new_base}{part}/{version_date}/{section}/", permanent=True
            )
    for pattern in [INTERP_INTRO_RE, INTERP_APPENDIX_RE, INTERP_SECTION_RE]:
        match_base = pattern.match(original_url)
        if match_base:
            doc = match_base.group(1)
            version_date = get_version_date(part, doc)
            if pattern == INTERP_INTRO_RE:
                if version_date:
                    return redirect(
                        f"{new_base}{part}/{version_date}/h1-interp/",
                        permanent=True,
                    )
                else:
                    return redirect(f"{new_base}{part}/interp-0/", permanent=True)
            if pattern == INTERP_APPENDIX_RE:
                appendix = INTERP_APPENDIX_DEFAULTS.get(part, "A")
                if version_date:
                    return redirect(
                        f"{new_base}{part}/{version_date}"
                        f"/interp-{appendix.lower()}/",
                        permanent=True,
                    )
                else:
                    return redirect(
                        f"{new_base}{part}/interp-{appendix.lower()}/",
                        permanent=True,
                    )
            if pattern == INTERP_SECTION_RE:
                section = INTERP_SECTION_DEFAULTS.get(part, "1")
                if version_date:
                    return redirect(
                        f"{new_base}{part}/{version_date}"
                        f"/interp-{section.lower()}/",
                        permanent=True,
                    )
                else:
                    return redirect(
                        f"{new_base}{part}/interp-{section.lower()}/",
                        permanent=True,
                    )
    # catch-all: we have a valid part, but we can't decipher more than that
    return redirect(f"{new_base}{part}/", permanent=True)
