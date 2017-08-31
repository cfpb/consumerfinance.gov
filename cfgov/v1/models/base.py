import csv
from collections import OrderedDict
from cStringIO import StringIO
from itertools import chain
from urllib import urlencode

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel, ObjectList,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore import blocks, hooks
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import (Orderable, Page, PageManager,
                                        PageQuerySet)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from v1 import get_protected_url
from v1.atomic_elements import molecules, organisms
from v1.models.snippets import ReusableText, ReusableTextChooserBlock
from v1.util import ref


class CFGOVAuthoredPages(TaggedItemBase):
    content_object = ParentalKey('CFGOVPage')

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class CFGOVTaggedPages(TaggedItemBase):
    content_object = ParentalKey('CFGOVPage')

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class BaseCFGOVPageManager(PageManager):
    def get_queryset(self):
        return PageQuerySet(self.model).order_by('path')

CFGOVPageManager = BaseCFGOVPageManager.from_queryset(PageQuerySet)


class CFGOVPage(Page):
    authors = ClusterTaggableManager(through=CFGOVAuthoredPages, blank=True,
                                     verbose_name='Authors',
                                     help_text='A comma separated list of '
                                               + 'authors.',
                                     related_name='authored_pages')
    tags = ClusterTaggableManager(through=CFGOVTaggedPages, blank=True,
                                  related_name='tagged_pages')
    shared = models.BooleanField(default=False)
    has_unshared_changes = models.BooleanField(default=False)
    language = models.CharField(
        choices=ref.supported_languagues, default='en', max_length=2
    )
    social_sharing_image = models.ForeignKey(
        'v1.CFGOVImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=(
            'Optionally select a custom image to appear when users share this '
            'page on social media websites. Minimum size: 1200w x 630h.'
        )
    )

    # This is used solely for subclassing pages we want to make at the CFPB.
    is_creatable = False

    objects = CFGOVPageManager()

    # These fields show up in either the sidebar or the footer of the page
    # depending on the page type.
    sidefoot = StreamField([
        ('call_to_action', molecules.CallToAction()),
        ('related_links', molecules.RelatedLinks()),
        ('related_posts', organisms.RelatedPosts()),
        ('related_metadata', molecules.RelatedMetadata()),
        ('email_signup', organisms.EmailSignUp()),
        ('sidebar_contact', organisms.SidebarContactInfo()),
        ('rss_feed', molecules.RSSFeed()),
        ('social_media', molecules.SocialMedia()),
        ('reusable_text', ReusableTextChooserBlock(ReusableText)),
    ], blank=True)

    # Panels
    promote_panels = Page.promote_panels + [
        ImageChooserPanel('social_sharing_image'),
    ]

    sidefoot_panels = [
        StreamFieldPanel('sidefoot'),
    ]

    settings_panels = [
        MultiFieldPanel(promote_panels, 'Settings'),
        InlinePanel('categories', label="Categories", max_num=2),
        FieldPanel('tags', 'Tags'),
        FieldPanel('authors', 'Authors'),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
        FieldPanel('language', 'language'),
    ]

    # Tab handler interface guide because it must be repeated for each subclass
    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar/Footer'),
        ObjectList(settings_panels, heading='Configuration'),
    ])

    def get_authors(self):
        """ Returns a sorted list of authors. Default is alphabetical """
        return self.alphabetize_authors()

    def alphabetize_authors(self):
        """
        Alphabetize authors of this page by last name,
        then first name if needed
        """
        # First sort by first name
        author_names = self.authors.order_by('name')
        # Then sort by last name
        return sorted(author_names, key=lambda x: x.name.split()[-1])

    def generate_view_more_url(self, request):
        activity_log = CFGOVPage.objects.get(slug='activity-log').specific
        tags = []
        index = activity_log.form_id()
        tags = urlencode([('filter%s_topics' % index, tag)
                          for tag in self.tags.slugs()])
        return (get_protected_url({'request': request}, activity_log)
                + '?' + tags)

    def related_posts(self, block):
        from v1.models.learn_page import AbstractFilterPage
        related = {}
        query = models.Q(('tags__name__in', self.tags.names()))
        search_types = [
            ('blog', 'posts', 'Blog', query),
            ('newsroom', 'newsroom', 'Newsroom', query),
            ('events', 'events', 'Events', query),
        ]

        def fetch_children_by_specific_category(block, parent_slug):
            """
            This used to be a Page.objects.get, which would throw
            an exception if the requested parent wasn't found. As of
            Django 1.6, you can now do Page.objects.filter().first();
            the advantage here is that you can check for None right
            away and not have to rely on catching exceptions, which
            in any case didn't do anything useful other than to print
            an error message. Instead, we just return an empty query
            which has no effect on the final result.
            """
            parent = Page.objects.filter(slug=parent_slug).first()
            if parent:
                child_query = Page.objects.child_of_q(parent)
                if 'specific_categories' in block.value:
                    child_query &= specific_categories_query(
                        block, parent_slug)
            else:
                child_query = Q()
            return child_query

        def specific_categories_query(block, parent_slug):
            specific_categories = ref.related_posts_category_lookup(
                block.value['specific_categories']
            )
            choices = [c[0] for c in ref.choices_for_page_type(parent_slug)]
            categories = [c for c in specific_categories if c in choices]
            if categories:
                return Q(('categories__name__in', categories))
            else:
                return Q()

        for parent_slug, search_type, search_type_name, search_query in \
                search_types:
            search_query &= fetch_children_by_specific_category(
                block, parent_slug)
            if parent_slug == 'events':
                search_query |= fetch_children_by_specific_category(
                    block, 'archive-past-events') & query
            relate = block.value.get('relate_{}'.format(search_type), None)
            if relate:
                type_query = (
                    AbstractFilterPage.objects.live().filter(
                        search_query
                    ).distinct().exclude(id=self.id).order_by(
                        '-date_published'
                    )
                )
                # Apply similar logic as snippets.py's filter_by_tags method
                # to enable AND filtering
                if block.value['and_filtering']:
                    for tag in self.tags.names():
                        type_query = type_query.filter(tags__name=tag)
                related[search_type_name] = type_query[:block.value['limit']]

        # Return a dictionary of lists of each type when there's at least one
        # hit for that type.
        return {search_type: queryset for search_type, queryset in
                related.items() if queryset}

    def get_breadcrumbs(self, request):
        ancestors = self.get_ancestors()
        home_page_children = request.site.root_page.get_children()
        for i, ancestor in enumerate(ancestors):
            if ancestor in home_page_children:
                return [ancestor for ancestor in ancestors[i + 1:]]
        return []

    def get_appropriate_descendants(self, hostname, inclusive=True):
        return CFGOVPage.objects.live().descendant_of(
            self, inclusive)

    def get_appropriate_siblings(self, hostname, inclusive=True):
        return CFGOVPage.objects.live().sibling_of(self, inclusive)

    def get_next_appropriate_siblings(self, hostname, inclusive=False):
        return self.get_appropriate_siblings(
            hostname=hostname, inclusive=inclusive).filter(
            path__gte=self.path).order_by('path')

    def get_prev_appropriate_siblings(self, hostname, inclusive=False):
        return self.get_appropriate_siblings(
            hostname=hostname, inclusive=inclusive).filter(
            path__lte=self.path).order_by('-path')

    def get_context(self, request, *args, **kwargs):
        context = super(CFGOVPage, self).get_context(request, *args, **kwargs)
        for hook in hooks.get_hooks('cfgovpage_context_handlers'):
            hook(self, request, context, *args, **kwargs)
        return context

    def serve(self, request, *args, **kwargs):
        """
        If request is ajax, then return the ajax request handler response, else
        return the super.
        """
        if request.method == 'POST':
            return self.serve_post(request, *args, **kwargs)

        # Force the page's language on the request
        translation.activate(self.language)
        request.LANGUAGE_CODE = translation.get_language()
        return super(CFGOVPage, self).serve(request, *args, **kwargs)

    def _return_bad_post_response(self, request):
        if request.is_ajax():
            return JsonResponse({'result': 'error'}, status=400)

        return HttpResponseBadRequest(self.url)

    def serve_post(self, request, *args, **kwargs):
        """Handle a POST to a specific form on the page.

        Attempts to retrieve form_id from the POST request, which must be
        formatted like "form-name-index" where the "name" part is the name of a
        StreamField on the page and the "index" part refers to the index of the
        form element in the StreamField.

        If form_id is found, it returns the response from the block method
        retrieval.

        If form_id is not found, it returns an error response.
        """
        form_module = None
        form_id = request.POST.get('form_id', None)

        if form_id:
            form_id_parts = form_id.split('-')

            if len(form_id_parts) == 3:
                streamfield_name = form_id_parts[1]
                streamfield = getattr(self, streamfield_name, None)

                if streamfield is not None:
                    try:
                        streamfield_index = int(form_id_parts[2])
                    except ValueError:
                        streamfield_index = None

                    try:
                        form_module = streamfield[streamfield_index]
                    except IndexError:
                        form_module = None

        if form_module is None:
            return self._return_bad_post_response(request)

        result = form_module.block.get_result(
            self,
            request,
            form_module.value,
            True
        )

        if isinstance(result, HttpResponse):
            return result

        context = self.get_context(request, *args, **kwargs)
        context['form_modules'][streamfield_name].update({
            streamfield_index: result
        })

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            context
        )

    class Meta:
        app_label = 'v1'

    def parent(self):
        parent = self.get_ancestors(inclusive=False).reverse()[0].specific
        return parent

    # To be overriden if page type requires JS files every time
    # 'template' is used as the key for front-end consistency
    def add_page_js(self, js):
        js['template'] = []

    # Retrieves the stream values on a page from it's Streamfield
    def _get_streamfield_blocks(self):
        lst = [value for key, value in vars(self).iteritems()
               if type(value) is StreamValue]
        return list(chain(*lst))

    # Gets the JS from the Streamfield data
    def _add_streamfield_js(self, js):
        # Create a dict with keys ordered organisms, molecules, then atoms
        for child in self._get_streamfield_blocks():
            self._add_block_js(child.block, js)

    # Recursively search the blocks and classes for declared Media.js
    def _add_block_js(self, block, js):
        self._assign_js(block, js)
        if (
            issubclass(type(block), blocks.StructBlock) or
            issubclass(type(block), blocks.StreamBlock)
        ):
            for child in block.child_blocks.values():
                self._add_block_js(child, js)
        elif issubclass(type(block), blocks.ListBlock):
            self._add_block_js(block.child_block, js)

    # Assign the Media js to the dictionary appropriately
    def _assign_js(self, obj, js):
        if hasattr(obj, 'Media') and hasattr(obj.Media, 'js'):
            for key in js.keys():
                if obj.__module__.endswith(key):
                    js[key] += obj.Media.js
            if not [key for key in js.keys()
                    if obj.__module__.endswith(key)]:
                js['other'] += obj.Media.js

    # Returns all the JS files specific to this page and it's current
    # Streamfield's blocks
    @property
    def media(self):
        js = OrderedDict()
        for key in ['template', 'organisms', 'molecules', 'atoms', 'other']:
            js.update({key: []})
        self.add_page_js(js)
        self._add_streamfield_js(js)
        for key, js_files in js.iteritems():
            js[key] = OrderedDict.fromkeys(js_files).keys()
        return js

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        return self.social_sharing_image


class CFGOVPageCategory(Orderable):
    page = ParentalKey(CFGOVPage, related_name='categories')
    name = models.CharField(max_length=255, choices=ref.categories)

    panels = [
        FieldPanel('name'),
    ]


# keep encrypted passwords around to ensure that user does not re-use
# any of the previous 10
class PasswordHistoryItem(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # password becomes invalid at...
    locked_until = models.DateTimeField()  # password cannot be changed until
    encrypted_password = models.CharField(_('password'), max_length=128)

    class Meta:
        get_latest_by = 'created'

    @classmethod
    def current_for_user(cls, user):
        return user.passwordhistoryitem_set.latest()

    def can_change_password(self):
        now = timezone.now()
        return(now > self.locked_until)

    def must_change_password(self):
        now = timezone.now()
        return(self.expires_at < now)


# User Failed Login Attempts
class FailedLoginAttempt(models.Model):
    user = models.OneToOneField(User)
    # comma-separated timestamp values, right now it's a 10 digit number,
    # so we can store about 91 last failed attempts
    failed_attempts = models.CharField(max_length=1000)

    def __unicode__(self):
        attempts_no = (0 if not self.failed_attempts
                       else len(self.failed_attempts.split(',')))
        return "%s has %s failed login attempts" % (self.user, attempts_no)

    def clean_attempts(self, timestamp):
        """ Leave only those that happened after <timestamp> """
        attempts = self.failed_attempts.split(',')
        self.failed_attempts = ','.join([fa for fa in attempts
                                         if int(fa) >= timestamp])

    def failed(self, timestamp):
        """ Add another failed attempt """
        attempts = (self.failed_attempts.split(',')
                    if self.failed_attempts else [])
        attempts.append(str(int(timestamp)))
        self.failed_attempts = ','.join(attempts)

    def too_many_attempts(self, value, timestamp):
        """ Compare number of failed attempts to <value> """
        self.clean_attempts(timestamp)
        attempts = self.failed_attempts.split(',')
        return len(attempts) > value


class TemporaryLockout(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


class Feedback(models.Model):
    submitted_on = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        Page,
        related_name='feedback',
        null=True,
        on_delete=models.SET_NULL,
    )
    comment = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=8, blank=True, null=True)
    referrer = models.CharField(max_length=255, blank=True, null=True)
    is_helpful = models.NullBooleanField()
    expect_to_buy = models.CharField(max_length=255, blank=True, null=True)
    currently_own = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)

    def assemble_csv(self, queryset):
        headings = [
            'comment',
            'currently_own',
            'expect_to_buy',
            'email',
            'is_helpful',
            'page',
            'referrer',
            'submitted_on',
            'language'
        ]
        csvfile = StringIO()
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow([field for field in headings])
        for feedback in queryset:
            feedback.submitted_on = "{}".format(feedback.submitted_on.date())
            feedback.comment = feedback.comment.encode('utf-8')
            writer.writerow(
                ["{}".format(getattr(feedback, heading))
                 for heading in headings]
            )
        return csvfile.getvalue()
