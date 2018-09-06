from __future__ import unicode_literals

import re

from django.http import Http404  # , HttpResponse, JsonResponse
from django.shortcuts import redirect  # , get_object_or_404, render

from dateutil import parser

from regulations3k.models import EffectiveVersion


# TODO
# search queries
# appendices
# interpretations

# Mapping of document number to effective date
VERSION_MAP = {
    '1002': {
        '2017-20417_20220101': '2022-01-01',
        # '2017-20417_20180101': '2018-01-01',  # current law
        '2016-16301': '2016-07-11',
        '2013-22752_20140118': '2014-01-18',
        '2013-22752_20140110': '2014-01-10',
        '2013-22752_20140101': '2014-01-01',
        '2011-31714': '2011-12-30',
    },
    '1003': {
        '2015-26607_20200101': '2020-01-01',
        '2015-26607_20190101': '2019-01-01',
        # '2017-18284_20180101': '2018-01-01',  # current law
        '2015-26607_20170101': '2017-01-01',
        '2016-30731': '2016-01-01',
        '2014-30404': '2015-01-01',
        '2013-31223': '2014-01-01',
        '2012-31311': '2012-12-31',
        '2012-3460': '2012-02-15',
        '2011-31712': '2011-12-30',
    },
    '1004': {
        # '2011-18676': '2011-07-22',  # current law
    },
    '1005': {
        '2018-01305': '2019-01-01',
        # '2016-24506': '2016-11-14',  # current law
        '2014-20681': '2014-11-17',
        '2013-19503': '2013-10-28',
        '2013-06861': '2013-03-26',
        '2011-31725': '2011-12-30',
    },
    '1010': {
        # '2016-10715': '2016-06-10',  # current law
        '2011-31713': '2011-12-30',
    },
    '1011': {
        # '2011-31713': '2011-12-30',  # current law
    },
    '1012': {
        # '2012-10602': '2012-05-03',  # current law
        '2011-31713': '2011-12-30',
    },
    '1013': {
        # '2017-24411': '2018-01-01',  # current law
        '2016-28710': '2017-01-01',
        '2015-30071': '2016-01-01',
        '2014-21847': '2015-01-01',
        '2013-28194': '2014-01-01',
        '2012-27996': '2013-01-01',
        '2011-31723': '2011-12-30',
    },
    '1024': {
        # '2017-21912': '2017-10-19',  # current law
        '2015-18239': '2015-10-03',
        '2013-15466': '2014-02-14',
        '2013-24521': '2014-01-10',
        '2013-09750': '2013-06-03',
        '2011-31722': '2011-12-30',
    },
    '1026': {
        '2018-01305': '2019-04-01',
        # '2018-09243': '2018-06-01',  # current law
        '2018-04823': '2018-04-19',
        '2017-24445': '2018-01-01',
        '2017-15764': '2017-10-10',
        '2016-24503': '2017-10-01',
        '2016-30730': '2017-01-01',
        '2016-14782_20160627': '2016-06-27',
        '2016-06834': '2016-03-31',
        '2015-32293': '2016-01-01',
        '2015-32463': '2015-12-24',
        '2015-18239': '2015-10-03',
        '2015-12719': '2015-08-10',
        '2013-30108_20150718': '2015-07-18',
        '2015-09000': '2015-04-17',
        '2014-30419': '2015-01-01',
        '2013-30108_20140118': '2014-01-18',
        '2013-24521': '2014-01-10',
        '2013-31225': '2014-01-01',
        '2013-16962_20130724': '2013-07-24',
        '2013-12125': '2013-06-01',
        '2013-10429': '2013-05-03',
        '2013-07066': '2013-03-28',
        '2012-27997': '2013-01-01',
        '2012-28341': '2012-11-23',
        '2011-31715': '2011-12-30',
    },
    '1030': {
        # '2011-31727': '2011-12-30',  # current law
    },
}


def redirect_eregs(request):
    """
    Redirect legacy eregulations pages to the relevant regulations3k page.

    Requests for past or future versions of a regulation will be sent to the
    current-law version in regulations3k, from which past versions will be
    available in the future.
    """
    original_base = '/eregulations/'
    new_base = '/policy-compliance/rulemaking/regulations/'
    reg_re = re.compile(r'/eregulations/(\d{4})$')
    part_re = re.compile(r'/eregulations/(\d{4})-(\d{1,3})/([0-9_-]+)')
    original_url = request.path
    if original_url == original_base:
        return redirect(new_base, permanent=True)
    reg_base = reg_re.match(original_url)
    if reg_base:
        return redirect(new_base + reg_base.group(1) + '/', permanent=True)
    part_base = part_re.match(original_url)
    if part_base:
        (part, section, doc) = (
            part_base.group(1), part_base.group(2), part_base.group(3))
        if part not in VERSION_MAP:
            raise Http404
        eff_date_string = VERSION_MAP[part].get(doc)
        if not eff_date_string:
            return redirect("{}{}/{}/".format(
                new_base, part, section), permanent=True)
        eff_date = parser.parse(eff_date_string).date()
        version = EffectiveVersion.objects.filter(
            part__part_number=part,
            effective_date=eff_date,
            draft=False).first()
        if version:
            return redirect("{}{}/{}/{}/".format(
                new_base, part, eff_date_string, section),
                permanent=True)
        return redirect("{}{}/{}/".format(new_base, part, section))
