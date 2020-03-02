import logging

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.utils.html import format_html_join

import wagtail
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from scripts import export_enforcement_actions

from ask_cfpb.models.snippets import GlossaryTerm
from v1.admin_views import ExportFeedbackView, manage_cdn
from v1.models.menu_item import MenuItem as MegaMenuItem
from v1.models.portal_topics import PortalCategory, PortalTopic
from v1.models.resources import Resource
from v1.models.snippets import Contact, RelatedResource, ReusableText
from v1.util import util


try:
    from wagtail.admin.menu import MenuItem
    from wagtail.core import hooks
    from wagtail.core.whitelist import attribute_rule
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin.menu import MenuItem
    from wagtail.wagtailcore import hooks
    from wagtail.wagtailcore.whitelist import attribute_rule


logger = logging.getLogger(__name__)


def export_data(request):
    if request.method == 'POST':
        return export_enforcement_actions.export_actions(http_response=True)
    return render(request, 'wagtailadmin/export_data.html')


@hooks.register('register_admin_menu_item')
def register_export_menu_item():
    return MenuItem(
        'Enforcement actions',
        reverse('export-enforcement-actions'),
        classnames='icon icon-download',
        order=99999,
    )


@hooks.register('register_admin_urls')
def register_export_url():
    return [url(
        'export-enforcement-actions',
        export_data,
        name='export-enforcement-actions')]


@hooks.register('before_delete_page')
def raise_delete_error(request, page):
    raise PermissionDenied('Deletion via POST is disabled')


@hooks.register('after_delete_page')
def log_page_deletion(request, page):
    logger.warning(
        (
            u'User {user} with ID {user_id} deleted page {title} '
            u'with ID {page_id} at URL {url}'
        ).format(
            user=request.user,
            user_id=request.user.id,
            title=page.title,
            page_id=page.id,
            url=page.url_path,
        )
    )


@hooks.register('insert_editor_js')
def editor_js():
    js_files = ['js/table-block.js']

    if wagtail.VERSION >= (2, 0):
        # js_files.insert(0, 'wagtailadmin/js/hallo-bootstrap.js')
        js_files.insert(0, 'wagtailadmin/js/vendor/hallo.js')
        js_files.insert(0, 'wagtailadmin/js/hallo-plugins/hallo-hr.js')
        js_files.insert(
            0,
            'wagtailadmin/js/hallo-plugins/hallo-requireparagraphs.js'
        )
        js_files.insert(
            0, 'wagtailadmin/js/hallo-plugins/hallo-wagtaillink.js')
        js_files.insert(
            0,
            'wagtaildocs/js/hallo-plugins/hallo-wagtaildoclink.js'
        )
        js_files.insert(
            0,
            'wagtailembeds/js/hallo-plugins/hallo-wagtailembeds.js'
        )
        js_files.insert(
            0,
            'wagtailimages/js/hallo-plugins/hallo-wagtailimage.js'
        )

    js_includes = format_html_join(
        '\n',
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes


@hooks.register('insert_editor_css')
def editor_css():
    css_files = [
        'css/bureau-structure.css',
        'css/deprecated-blocks.css',
        'css/general-enhancements.css',
        'css/heading-block.css',
        'css/table-block.css',
    ]

    if wagtail.VERSION >= (2, 0):
        css_files.insert(0, 'wagtailadmin/css/panels/hallo.css')

    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files)
    )

    return css_includes


@hooks.register('cfgovpage_context_handlers')
def form_module_handlers(page, request, context, *args, **kwargs):
    """
    Hook function that iterates over every Streamfield's blocks on a page and
    sets the context for any form modules.
    """
    form_modules = {}
    streamfields = util.get_streamfields(page)

    for fieldname, blocks in streamfields.items():
        for index, child in enumerate(blocks):
            if hasattr(child.block, 'get_result'):
                if fieldname not in form_modules:
                    form_modules[fieldname] = {}

                if not request.method == 'POST':
                    is_submitted = child.block.is_submitted(
                        request,
                        fieldname,
                        index
                    )
                    module_context = child.block.get_result(
                        page,
                        request,
                        child.value,
                        is_submitted
                    )
                    form_modules[fieldname].update({index: module_context})
    if form_modules:
        context['form_modules'] = form_modules


class PermissionCheckingMenuItem(MenuItem):
    """
    MenuItem that only displays if the user has a certain permission.

    This subclassing approach is recommended by the Wagtail documentation:
    https://docs.wagtail.io/en/v1.13.4/reference/hooks.html#register-admin-menu-item
    """

    def __init__(self, *args, **kwargs):
        self.permission = kwargs.pop('permission')
        super(PermissionCheckingMenuItem, self).__init__(*args, **kwargs)

    def is_shown(self, request):
        return request.user.has_perm(self.permission)


@hooks.register('register_admin_menu_item')
def register_export_feedback_menu_item():
    return PermissionCheckingMenuItem(
        'Export feedback',
        reverse('export-feedback'),
        classnames='icon icon-download',
        order=99999,
        permission='v1.export_feedback'
    )


@hooks.register('register_admin_menu_item')
def register_django_admin_menu_item():
    return MenuItem(
        'Django Admin',
        reverse('admin:index'),
        classnames='icon icon-redirect',
        order=99999
    )


@hooks.register('register_admin_menu_item')
def register_frank_menu_item():
    return MenuItem('CDN Tools',
                    reverse('manage-cdn'),
                    classnames='icon icon-cogs',
                    order=10000)


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^cdn/$', manage_cdn, name='manage-cdn'),
        url(r'^export-feedback/$',
            ExportFeedbackView.as_view(),
            name='export-feedback'),
    ]


@hooks.register('before_serve_page')
def serve_latest_draft_page(page, request, args, kwargs):
    if page.pk in settings.SERVE_LATEST_DRAFT_PAGES:
        latest_draft = page.get_latest_revision_as_page()
        response = latest_draft.serve(request, *args, **kwargs)
        response['Serving-Wagtail-Draft'] = '1'
        return response


@hooks.register('before_serve_shared_page')
def before_serve_shared_page(page, request, args, kwargs):
    request.show_draft_megamenu = True


class MegaMenuModelAdmin(ModelAdmin):
    model = MegaMenuItem
    menu_label = 'Mega Menu'
    menu_icon = 'cog'
    list_display = ('link_text', 'order')


modeladmin_register(MegaMenuModelAdmin)


@receiver(post_save, sender=MegaMenuItem)
def clear_mega_menu_cache(sender, instance, **kwargs):
    from django.core.cache import caches
    caches['default_fragment_cache'].delete('mega_menu')


def get_resource_tags():
    tag_list = []

    for resource in Resource.objects.all():
        for tag in resource.tags.all():
            tuple = (tag.slug, tag.name)
            if tuple not in tag_list:
                tag_list.append(tuple)

    return sorted(tag_list, key=lambda tup: tup[0])


class ResourceTagsFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'tags'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return get_resource_tags()

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        for tag in get_resource_tags():
            if self.value() == tag[0]:
                return queryset.filter(tags__slug__iexact=tag[0])


class ResourceModelAdmin(ModelAdmin):
    model = Resource
    menu_label = 'Resources'
    menu_icon = 'snippet'
    list_display = ('title', 'desc', 'order', 'thumbnail')
    ordering = ('title',)
    list_filter = (ResourceTagsFilter,)
    search_fields = ('title',)


class ContactModelAdmin(ModelAdmin):
    model = Contact
    menu_icon = 'snippet'
    list_display = ('heading', 'body')
    ordering = ('heading',)
    search_fields = ('heading', 'body', 'contact_info')


class PortalTopicModelAdmin(ModelAdmin):
    model = PortalTopic
    menu_icon = 'snippet'
    list_display = ('heading', 'heading_es')
    ordering = ('heading',)
    search_fields = ('heading', 'heading_es')


class PortalCategoryModelAdmin(ModelAdmin):
    model = PortalCategory
    menu_icon = 'snippet'
    list_display = ('heading', 'heading_es')
    ordering = ('heading',)
    search_fields = ('heading', 'heading_es')


class ReusableTextModelAdmin(ModelAdmin):
    model = ReusableText
    menu_icon = 'snippet'
    list_display = ('title', 'sidefoot_heading', 'text')
    ordering = ('title',)
    search_fields = ('title', 'sidefoot_heading', 'text')


class RelatedResourceModelAdmin(ModelAdmin):
    model = RelatedResource
    menu_icon = 'snippet'
    list_display = ('title', 'text')
    ordering = ('title',)
    search_fields = ('title', 'text')


class GlossaryTermModelAdmin(ModelAdmin):
    model = GlossaryTerm
    menu_icon = 'snippet'
    list_display = ('name_en', 'definition_en', 'portal_topic')
    ordering = ('name_en',)
    search_fields = ('name_en', 'definition_en', 'name_es', 'definition_es')


class SnippetModelAdminGroup(ModelAdminGroup):
    menu_label = 'Snippets'
    menu_icon = 'snippet'
    menu_order = 400
    items = (
        ContactModelAdmin,
        ResourceModelAdmin,
        ReusableTextModelAdmin,
        RelatedResourceModelAdmin,
        PortalTopicModelAdmin,
        PortalCategoryModelAdmin,
        GlossaryTermModelAdmin)


modeladmin_register(SnippetModelAdminGroup)


# Hide default Snippets menu item
@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items
                     if item.url != reverse('wagtailsnippets:index')]


# Override list of allowed tags in a RichTextField
@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    allow_html_class = attribute_rule({
        'class': True,
        'itemprop': True,
        'itemscope': True,
        'itemtype': True,
    })

    allowed_tags = ['aside', 'h4', 'h3', 'p', 'span',
                    'table', 'tr', 'th', 'td', 'tbody', 'thead', 'tfoot',
                    'col', 'colgroup']

    return {tag: allow_html_class for tag in allowed_tags}


@hooks.register('before_serve_shared_page')
def set_served_by_wagtail_sharing(page, request, args, kwargs):
    setattr(request, 'served_by_wagtail_sharing', True)


@hooks.register('register_permissions')
def add_export_feedback_permission_to_wagtail_admin_group_view():
    return Permission.objects.filter(
        content_type__app_label='v1',
        codename='export_feedback'
    )
