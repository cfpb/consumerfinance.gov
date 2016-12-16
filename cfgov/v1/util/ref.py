limited_categories = [
    ('speech-bubble', 'Blog'),
    ('newspaper', 'Newsroom'),
    ('document', 'Report'),
    ('date', 'Events'),
    ('microphone', 'Speech'),
    ('bullhorn', 'Press Release'),
    ('contract', 'Op-Ed'),
    ('double-quote', 'Testimony'),
]

related_posts_categories = [
    ('Blog', (
        ('At the CFPB', 'At the CFPB'),
        ('Policy &amp; Compliance', 'Policy & Compliance'),
        ('Data, Research &amp; Reports', 'Data, research & reports'),
        ('Info for Consumers', 'Info for consumers'),
    )),
    ('Newsroom', (
        ('Op-Ed', 'Op-Ed'),
        ('Press Release', 'Press Release'),
        ('Speech', 'Speech'),
        ('Testimony', 'Testimony'),
    )),
]

page_types = [
    ('activity-log', 'Activity Log'),
    ('amicus-brief', 'Amicus Brief'),
    ('blog', 'Blog'),
    ('enforcement', 'Enforcement Action'),
    ('final-rule', 'Final Rule'),
    ('foia-freq-req-record', 'FOIA Frequently Requested Record'),
    ('impl-resource', 'Implementation Resource'),
    ('leadership-calendar', 'Leadership Calendar'),
    ('newsroom', 'Newsroom'),
    ('notice-opportunity-comment', 'Notice and Opportunity for Comment'),
    ('research-reports', 'Research Report'),
    ('rule-under-dev', 'Rule Under Development'),
    ('story', 'Story'),
]

fcm_types = [
    ('featured-event', 'Featured event'),
    ('featured-blog', 'Featured blog'),
    ('featured-video', 'Featured video'),
    ('featured-tool', 'Featured tool'),
    ('featured-news', 'Featured news'),
    ('featured', 'Featured'),
]

categories = [
    ('Amicus Brief', (
        ('us-supreme-court', 'U.S. Supreme Court'),
        ('fed-circuit-court', 'Federal Circuit Court'),
        ('fed-district-court', 'Federal District Court'),
        ('state-court', 'State Court'),
    )),
    ('Blog', (
        ('at-the-cfpb', 'At the CFPB'),
        ('policy_compliance', 'Policy & Compliance'),
        ('data-research-reports', 'Data, research & reports'),
        ('info-for-consumers', 'Info for consumers'),
    )),
    ('Enforcement action', (
        ('fed-district-case', 'Federal District Court Case'),
        ('admin-filing', 'Administrative Filing'),
    )),
    ('Final Rule', (
        ('interim-final-rule', 'Interim Final Rule'),
        ('final-rule', 'Final Rule'),
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
        ('op-ed', 'Op-Ed'),
        ('press-release', 'Press Release'),
        ('speech', 'Speech'),
        ('testimony', 'Testimony'),
    )),
    ('Notice and Opportunity for Comment', (
        ('notice-proposed-rule', 'Advanced Notice of Proposed Rulemaking'),
        ('proposed-rule', 'Proposed Rule'),
        ('interim-final-rule-2', 'Interim Final Rule'),
        ('request-comment-info', 'Request for Comment or Information'),
        ('proposed-policy', 'Proposed Policy'),
        ('intent-preempt-determ', 'Intent to make Preemption Determination'),
        ('info-collect-activity', 'Information Collection Activities'),
        ('notice-privacy-act', 'Notice related to Privacy Act'),
    )),
    ('Research Report', (
        ('consumer-complaint', 'Consumer Complaint'),
        ('super-highlight', 'Supervisory Highlights'),
        ('data-point', 'Data Point'),
        ('industry-markets', 'Industry and markets'),
        ('consumer-edu-empower', 'Consumer education and empowerment'),
        ('to-congress', 'To Congress'),
    )),
    ('Rule under development', (
        ('notice-proposed-rule-2', 'Advanced Notice of Proposed Rulemaking'),
        ('proposed-rule-2', 'Proposed Rule'),
    )),
    ('Story', (
        ('auto-loans', 'Auto loans'),
        ('credit-cards', 'Credit cards'),
        ('credit-reporting', 'Credit reporting'),
        ('debt-collection', 'Debt collection'),
        ('mortgages', 'Mortgages'),
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
        ('Activity Log', (
            ('blog', 'Blog'),
            ('op-ed', 'Op-Ed'),
            ('press-release', 'Press Release'),
            ('research-reports', 'Report'),
            ('speech', 'Speech'),
            ('testimony', 'Testimony'))),
        ('Leadership Calendar', (
            ('richard-cordray', 'Richard Cordray'),
            ('david-silberman', 'David Silberman'),
            ('meredith-fuchs', 'Meredith Fuchs'),
            ('steve-antonakes', 'Steve Antonakes'),
            ('raj-date', 'Raj Date'),
            ('elizabeth-warren', 'Elizabeth Warren'))),
        ('Newsroom', (
            ('blog', 'Blog'),
            ('op-ed', 'Op-Ed'),
            ('press-release', 'Press Release'),
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


def fcm_label(category):
    for slug, name in fcm_types:
        if slug == category:
            return name


def is_blog(page):
    for category in page.categories.all():
        for choice in choices_for_page_type('blog'):
            if category.name == choice[0]:
                return True
    if 'Blog' in page.specific_class.__name__:
        return True


def is_report(page):
    for category in page.categories.all():
        for choice in choices_for_page_type('research-reports'):
            if category.name == choice[0]:
                return True
