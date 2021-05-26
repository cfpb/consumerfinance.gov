import itertools


limited_categories = [
    ('speech-bubble', 'Blog'),
    ('newspaper', 'Newsroom'),
    ('document', 'Report'),
    ('pencil', "Director's notebook"),
    ('date', 'Events'),
    ('microphone', 'Speech'),
    ('bullhorn', 'Press release'),
    ('contract', 'Op-ed'),
    ('double-quote', 'Testimony'),
]

related_posts_categories = [
    ('Blog', (
        ('At the CFPB', 'At the CFPB'),
        ("Director's notebook", "Director's notebook"),
        ('Policy &amp; Compliance', 'Policy and compliance'),
        ('Data, Research &amp; Reports', 'Data, research, and reports'),
        ('Info for Consumers', 'Info for consumers'),
    )),
    ('Newsroom', (
        ('Op-Ed', 'Op-ed'),
        ('Press Release', 'Press release'),
        ('Speech', 'Speech'),
        ('Testimony', 'Testimony'),
    )),
]

page_types = [
    ('activity-log', 'Recent updates'),
    ('administrative-adjudication', 'Administrative adjudication'),
    ('amicus-brief', 'Amicus Brief'),
    ('blog', 'Blog'),
    ('consumer-reporting', 'Consumer Reporting Companies'),
    ('enforcement', 'Enforcement Action'),
    ('final-rule', 'Final rule'),
    ('foia-freq-req-record', 'FOIA Frequently Requested Record'),
    ('impl-resource', 'Implementation Resource'),
    ('leadership-calendar', 'Leadership Calendar'),
    ('newsroom', 'Newsroom'),
    ('notice-opportunity-comment', 'Notice and Opportunity for Comment'),
    ('research-reports', 'Research Report'),
    ('rule-under-dev', 'Rule Under Development'),
    ('story', 'Story'),
    ('ask', 'Ask CFPB'),
    ('cfpb-researchers', 'CFPB Researchers'),
]

categories = [
    ('Administrative adjudication docket', (
        ('administrative-adjudication', 'Administrative adjudication'),
        ('stipulation-and-constent-order', 'Stipulation and consent order'),
    )),
    ('Amicus Brief', (
        ('us-supreme-court', 'U.S. Supreme Court'),
        ('fed-circuit-court', 'Federal Circuit Court'),
        ('fed-district-court', 'Federal District Court'),
        ('state-court', 'State Court'),
    )),
    ('Blog', (
        ('at-the-cfpb', 'At the CFPB'),
        ('directors-notebook', "Director's notebook"),
        ('policy_compliance', 'Policy and compliance'),
        ('data-research-reports', 'Data, research, and reports'),
        ('info-for-consumers', 'Info for consumers'),
    )),
    ('Consumer Reporting Companies', (
        ('nationwide', 'Nationwide'),
        ('employment-screening', 'Employment screening'),
        ('tenant-screening', 'Tenant screening'),
        ('check-bank-screening', 'Check and bank screening'),
        ('personal-property-insurance', 'Personal property insurance'),
        ('medical', 'Medical'),
        ('low-income-and-subprime', 'Low-income and subprime'),
        ('supplementary-reports', 'Supplementary reports'),
        ('utilities', 'Utilities'),
        ('retail', 'Retail'),
        ('gaming', 'Gaming'),
    )),
    ('Enforcement Action', (
        ('administrative-proceeding', 'Administrative Proceeding'),
        ('civil-action', 'Civil Action'),
    )),
    ('Final rule', (
        ('interim-final-rule', 'Interim final rule'),
        ('final-rule', 'Final rule'),
    )),
    ('FOIA Frequently Requested Record', (
        ('report', 'Report'),
        ('log', 'Log'),
        ('record', 'Record'),
    )),
    ('Implementation Resource', (
        ('compliance-aid', 'Compliance aid'),
        ('official-guidance', 'Official guidance'),
    )),
    ('Newsroom', (
        ('op-ed', 'Op-ed'),
        ('press-release', 'Press release'),
        ('speech', 'Speech'),
        ('testimony', 'Testimony'),
    )),
    ('Notice and Opportunity for Comment', (
        ('notice-proposed-rule', 'Advance notice of proposed rulemaking'),
        ('proposed-rule', 'Proposed rule'),
        ('interim-final-rule-2', 'Interim final rule'),
        ('request-comment-info', 'Request for comment or information'),
        ('proposed-policy', 'Proposed policy'),
        ('intent-preempt-determ', 'Intent to make preemption determination'),
        ('info-collect-activity', 'Information collection activities'),
        ('notice-privacy-act', 'Notice related to Privacy Act'),
    )),
    ('Research Report', (
        ('consumer-complaint', 'Consumer complaint'),
        ('super-highlight', 'Supervisory Highlights'),
        ('data-point', 'Data point'),
        ('industry-markets', 'Industry and markets'),
        ('consumer-edu-empower', 'Consumer education and empowerment'),
        ('to-congress', 'To Congress'),
    )),
    ('Rule Under Development', (
        ('notice-proposed-rule-2', 'Advance notice of proposed rulemaking'),
        ('proposed-rule-2', 'Proposed rule'),
    )),
    ('Story', (
        ('auto-loans', 'Auto loans'),
        ('bank-accts-services', 'Bank accounts and services'),
        ('credit-cards', 'Credit cards'),
        ('credit-reports-scores', 'Credit reports and scores'),
        ('debt-collection', 'Debt collection'),
        ('money-transfers', 'Money transfers'),
        ('mortgages', 'Mortgages'),
        ('payday-loans', 'Payday loans'),
        ('prepaid-cards', 'Prepaid cards'),
        ('student-loans', 'Student loans'),
    )),
]

supported_languagues = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('zh', 'Chinese'),
    ('vi', 'Vietnamese'),
    ('ko', 'Korean'),
    ('tl', 'Tagalog'),
    ('ru', 'Russian'),
    ('ar', 'Arabic'),
    ('ht', 'Haitian Creole'),
]


def get_appropriate_categories(specific_categories, page_type):
    """ An array of specific categories is provided from whatever
    is selected in the admin for related posts, however they each
    correspond to a page type, e.g. newsroom or blog. This function returns
    only the categories that belong to the page type in question
    """
    # Convert the provided categories to their slugs
    category_slugs = related_posts_category_lookup(specific_categories)
    # Look up the available categories for the page type in question
    options = [c[0] for c in choices_for_page_type(page_type)]

    return [c for c in category_slugs if c in options]


def related_posts_category_lookup(related_categories):
    related = []
    for category in related_categories:
        for name, related_posts_cats in related_posts_categories:
            for cat in related_posts_cats:
                if category == cat[0]:
                    related.append(cat[1])
    results = []
    for r in related:
        for name, cats in categories:
            for c in cats:
                if r == c[1]:
                    results.append(c[0])
    return results


def page_type_choices():
    new_choices = [
        ('Recent updates', (
            ('blog', 'Blog'),
            ('op-ed', 'Op-ed'),
            ('press-release', 'Press release'),
            ('research-reports', 'Report'),
            ('speech', 'Speech'),
            ('testimony', 'Testimony'))),
        ('Administrative adjudication', (
            ('administrative-adjudication', 'Administrative adjudication'),
            (
                'stipulation-and-constent-order',
                'Stipulation and consent order'
            )
        )),
        ('Leadership Calendar', (
            ('richard-cordray', 'Richard Cordray'),
            ('david-silberman', 'David Silberman'),
            ('meredith-fuchs', 'Meredith Fuchs'),
            ('steve-antonakes', 'Steve Antonakes'),
            ('raj-date', 'Raj Date'),
            ('elizabeth-warren', 'Elizabeth Warren'))),
        ('Newsroom', (
            ('op-ed', 'Op-ed'),
            ('press-release', 'Press release'),
            ('speech', 'Speech'),
            ('testimony', 'Testimony'))),
    ]
    categories_copy = list(categories)
    for i, category in enumerate(categories_copy):
        for choice in new_choices:
            if choice[0] == category[0]:
                del categories_copy[i]
    return sorted(categories + new_choices)


def choices_for_page_type(page_type):
    for slug, name in page_types:
        if page_type == slug:
            for cat_slug, cat_tuples in page_type_choices():
                if name == cat_slug:
                    return list(cat_tuples)
    return []


def category_label(category):
    for parent, children in page_type_choices():
        for slug, name in children:
            if category == slug:
                return name


def is_blog(page):
    for category in page.categories.all():
        for choice in choices_for_page_type('blog'):
            if category.name == choice[0]:
                return True
    if 'Blog' in page.specific_class.__name__:
        return True


def is_event(page):
    if 'Event' in page.specific_class.__name__:
        return True


def is_report(page):
    for category in page.categories.all():
        for choice in choices_for_page_type('research-reports'):
            if category.name == choice[0]:
                return True


def filterable_list_page_types():
    return page_types


def get_category_children(category_names):
    """Return a list of page category slugs for given category names."""
    categories_dict = dict(categories)
    return sorted(itertools.chain(*(
        dict(categories_dict[category]).keys()
        for category in category_names
    )))
