page_types = [
    ('amicus-brief', 'Amicus Brief'),
    ('blog', 'Blog'),
    ('enforcement', 'Enforcement action'),
    ('final-rule', 'Final Rule'),
    ('foia-freq-req-record', 'FOIA Frequently Requested Record'),
    ('impl-resource', 'Implementation Resource'),
    ('newsroom', 'Newsroom'),
    ('notice-opportunity-comment', 'Notice and Opportunity for Comment'),
    ('research-report', 'Research Report'),
    ('rule-under-dev', 'Rule under development'),
    ('leadership-calendar', 'Leadership Calendar'),
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
        ('cfpb_report', 'CFPB Report'),
        ('data-research-reports', 'Data, research & reports'),
        ('info-for-consumers', 'Info for consumers'),
    )),
    ('Enforcement action', (
        ('fed-district-case', 'Federal District Court Case'),
        ('admin-adj-process', 'Administrative Adjudication Process'),
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
        ('cfpb-bulletins-statements', 'CFPB Bulletins and Statements'),
        ('impl-compl-material', 'Implementation and Compliance Material'),
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
        ('snapshot', 'Snapshot'),
        ('consumer-voices', 'Consumer Voices'),
        ('education-programs', 'Education and Programs'),
        ('our-regulations', 'Our Regulations'),
        ('industry-practices', 'Industry Practices'),
        ('joint-reports', 'Joint Reports'),
        ('finances-results', 'Finances and Results'),
    )),
    ('Rule under development', (
        ('notice-proposed-rule-2', 'Advanced Notice of Proposed Rulemaking'),
        ('proposed-rule-2', 'Proposed Rule'),
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


def page_type_choices():
    new_choices = [
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
    return sorted(categories + new_choices)


def choices_for_page_type(page_type):
    for slug, name in page_types:
        if page_type == slug:
            for cat_slug, cat_tuples in page_type_choices():
                if name == cat_slug:
                    return list(cat_tuples)


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
        for blog_category in choices_for_page_type('blog'):
            if category.name == blog_category[0]:
                return True
