from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.response import TemplateResponse
from django.utils import timezone, translation
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel,
    TabbedInterface
)
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import (
    Orderable, Page, PageManager, PageQuerySet
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtailinventory.helpers import get_page_blocks

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.snippets import ReusableText
from v1.util import ref
from v1.util.util import validate_social_sharing_image


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
            'page on social media websites. Recommended size: 1200w x 630h. '
            'Maximum size: 4096w x 4096h.'
        )
    )

    # This is used solely for subclassing pages we want to make at the CFPB.
    is_creatable = False

    objects = CFGOVPageManager()

    search_fields = Page.search_fields + [
        index.SearchField('sidefoot'),
    ]

    # These fields show up in either the sidebar or the footer of the page
    # depending on the page type.
    sidefoot = StreamField([
        ('call_to_action', molecules.CallToAction()),
        ('related_links', molecules.RelatedLinks()),
        ('related_posts', organisms.RelatedPosts()),
        ('related_metadata', molecules.RelatedMetadata()),
        ('enforcement_action_metadata', molecules.EnforcementActionMetadata()),
        ('email_signup', organisms.EmailSignUp()),
        ('sidebar_contact', organisms.SidebarContactInfo()),
        ('rss_feed', molecules.RSSFeed()),
        ('social_media', molecules.SocialMedia()),
        ('reusable_text', v1_blocks.ReusableTextChooserBlock(ReusableText)),
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

    def clean(self):
        super(CFGOVPage, self).clean()
        validate_social_sharing_image(self.social_sharing_image)

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

    def related_metadata_tags(self):
        # Set the tags to correct data format
        tags = {'links': []}
        filter_page = self.get_filter_data()
        for tag in self.specific.tags.all():
            tag_link = {'text': tag.name, 'url': ''}
            if filter_page:
                relative_url = filter_page.relative_url(filter_page.get_site())
                param = '?topics=' + tag.slug
                tag_link['url'] = relative_url + param
            tags['links'].append(tag_link)
        return tags

    def get_filter_data(self):
        for ancestor in self.get_ancestors().reverse().specific():
            if ancestor.specific_class.__name__ in ['BrowseFilterablePage',
                                                    'SublandingFilterablePage',
                                                    'EventArchivePage',
                                                    'NewsroomLandingPage']:
                return ancestor
        return None

    def get_breadcrumbs(self, request):
        ancestors = self.get_ancestors()
        home_page_children = request.site.root_page.get_children()
        for i, ancestor in enumerate(ancestors):
            if ancestor in home_page_children:
                # Add top level parent page and `/process/` url segments
                # where necessary to BAH page breadcrumbs.
                # TODO: Remove this when BAH moves under /consumer-tools
                # and redirects are added after 2018 homebuying campaign.
                if ancestor.slug == 'owning-a-home':
                    breadcrumbs = []
                    for ancestor in ancestors[i:]:
                        ancestor_url = ancestor.relative_url(request.site)
                        if ancestor_url.startswith((
                                '/owning-a-home/prepare',
                                '/owning-a-home/explore',
                                '/owning-a-home/compare',
                                '/owning-a-home/close',
                                '/owning-a-home/sources')):
                            ancestor_url = ancestor_url.replace(
                                'owning-a-home', 'owning-a-home/process')
                        breadcrumbs.append({
                            'title': ancestor.title,
                            'href': ancestor_url,
                        })
                    return breadcrumbs
                # END TODO
                return [ancestor for ancestor in ancestors[i + 1:]]
        return []

    def get_appropriate_descendants(self, inclusive=True):
        return CFGOVPage.objects.live().descendant_of(
            self, inclusive)

    def get_appropriate_siblings(self, inclusive=True):
        return CFGOVPage.objects.live().sibling_of(self, inclusive)

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
    @property
    def page_js(self):
        return []

    @property
    def streamfield_js(self):
        js = []

        block_cls_names = get_page_blocks(self)
        for block_cls_name in block_cls_names:
            block_cls = import_string(block_cls_name)
            if hasattr(block_cls, 'Media') and hasattr(block_cls.Media, 'js'):
                js.extend(block_cls.Media.js)

        return js

    # Returns the JS files required by this page and its StreamField blocks.
    @property
    def media(self):
        return sorted(set(self.page_js + self.streamfield_js))

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        return self.social_sharing_image

    @property
    def post_preview_cache_key(self):
        return 'post_preview_{}'.format(self.id)


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
