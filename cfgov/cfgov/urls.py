from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from sheerlike.views.generic import SheerTemplateView
from sheerlike.feeds import SheerlikeFeed

from v1.views import LeadershipCalendarPDFView, EventICSView, unshare

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/pages/(\d+)/unshare/$', unshare, name='unshare'),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    # url(r'^search/$', 'search.views.search', name='search'),

    url(r'^$', SheerTemplateView.as_view(), name='home'),

    url(r'^docs/', include([
        url(r'^$', SheerTemplateView.as_view(template_name='docs_index.html'), name='index'),

        url(r'^sheer-layouts/', include([
            url(r'^$', SheerTemplateView.as_view(template_name='sheer-layouts/index.html'), name='index'),
            url(r'^jinja-content-blocks/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/jinja-content-blocks/index.html'),
                name='jinja-content-blocks'),
            url(r'^content-base/$', SheerTemplateView.as_view(template_name='sheer-layouts/content-base/index.html'),
                name='content-base'),
            url(r'^content-base-main-first/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/content-base-main-first/index.html'),
                name='content-base-main-first'),
            url(r'^content-base-sidebar-first/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/content-base-sidebar-first/index.html'),
                name='content-base-sidebar-first'),
            url(r'^layout-1-3/$', SheerTemplateView.as_view(template_name='sheer-layouts/layout-1-3/index.html'),
                name='layout-1-3'),
            url(r'^layout-side-nav/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/layout-side-nav/index.html'),
                name='layout-side-nav'),
            url(r'^layout-2-1/$', SheerTemplateView.as_view(template_name='sheer-layouts/layout-2-1/index.html'),
                name='layout-2-1'),
            url(r'^layout-2-1-bleedbar/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/layout-2-1-bleedbar/index.html'),
                name='layout-2-1-bleedbar'),
            url(r'^hero/$', SheerTemplateView.as_view(template_name='sheer-layouts/hero/index.html'),
                name='hero'),
        ],
            namespace='sheer-layouts')),

        url(r'^blog-docs/$', SheerTemplateView.as_view(template_name='blog-docs/index.html'), name='blog-docs'),
        url(r'^cf-enhancements/$', SheerTemplateView.as_view(template_name='cf-enhancements/index.html'),
            name='cf-enhancements'),
        url(r'^forms/$', SheerTemplateView.as_view(template_name='forms/index.html'), name='doc-forms'),
        url(r'^header/$', SheerTemplateView.as_view(template_name='header/index.html'), name='doc-header'),
        url(r'^lists/$', SheerTemplateView.as_view(template_name='lists/index.html'), name='doc-lists'),
        url(r'^media/$', SheerTemplateView.as_view(template_name='media/index.html'), name='doc-media'),
        url(r'^media-object/$', SheerTemplateView.as_view(template_name='media/index.html'), name='doc-media-object'),
        url(r'^meta/$', SheerTemplateView.as_view(template_name='meta/index.html'), name='doc-meta'),
        url(r'^misc/$', SheerTemplateView.as_view(template_name='misc/index.html'), name='doc-misc'),
        url(r'^nav-secondary/$', SheerTemplateView.as_view(template_name='nav-secondary/index.html'),
            name='nav-secondary'),
        url(r'^post/$', SheerTemplateView.as_view(template_name='post/index.html'), name='doc-post'),
        url(r'^print/$', SheerTemplateView.as_view(template_name='print/index.html'), name='doc-print'),
        url(r'^summary/$', SheerTemplateView.as_view(template_name='summary/index.html'), name='doc-summary'),

    ],
        namespace='docs')),

    url(r'^blog/', include([
        url(r'^$', TemplateView.as_view(template_name='blog/index.html'),
            name='index'),
        url(r'^(?P<doc_id>[\w-]+)/$',
            SheerTemplateView.as_view(doc_type='posts',
                                      local_name='post',
                                      default_template='blog/_single.html'),
            name='detail')],
        namespace='blog')),

    url(r'^newsroom/', include([
        url(r'^$', TemplateView.as_view(template_name='newsroom/index.html'),
            name='index'),
        url(r'^press-resources/$',
            TemplateView.as_view(
                template_name='newsroom/press-resources/index.html'),
            name='press-resources'),
        url(r'^(?P<doc_id>[\w-]+)/$',
            SheerTemplateView.as_view(doc_type='newsroom',
                                      local_name='newsroom',
                                      default_template='newsroom/_single.html'),
            name='detail')],
        namespace='newsroom')),

    url(r'^budget/', include([
        url(r'^$',
            TemplateView.as_view(template_name='budget/index.html'),
            name='home'),
        url(r'^(?P<page_slug>[\w-]+)/$',
            SheerTemplateView.as_view(),
            name='page')],
        namespace="budget")),

    url(r'^the-bureau/', include([
        url(r'^$', SheerTemplateView.as_view(template_name='the-bureau/index.html'),
            name='index'),
        url(r'^(?P<page_slug>[\w-]+)/$',
            SheerTemplateView.as_view(),
            name='page'),
        url(r'^leadership-calendar/pdf/$',
            LeadershipCalendarPDFView.as_view(),
            name='leadership-calendar-pdf'),
        url(r'^leadership-calendar/print/$',
            SheerTemplateView.as_view(),
            name='leadership-calendar-print')],
        namespace='the-bureau')),

    url(r'^doing-business-with-us/', include([
        url(r'^$',
            TemplateView.as_view(template_name='doing-business-with-us/index.html'),
            name='index'),
        url(r'^(?P<page_slug>[\w-]+)/$',
            SheerTemplateView.as_view(),
            name='page')],
        namespace='business')),

    url(r'^contact-us/', include([
        url(r'^$',
            TemplateView.as_view(template_name='contact-us/index.html'),
            name='index')],
        namespace='contact-us')),

    url(r'^events/', include([
        url(r'^$', TemplateView.as_view(template_name='events/index.html'),
            name='events'),
        url(r'^(?P<doc_id>[\w-]+)/$',
            SheerTemplateView.as_view(doc_type='events',
                                      local_name='event',
                                      default_template='events/_single.html'),
            name='event'),
        url(r'^(?P<doc_id>[\w-]+)/ics/$', EventICSView.as_view())],
        namespace='events')),

    url(r'^offices/', include([
        url(r'^(?P<doc_id>[\w-]+)/$',
            SheerTemplateView.as_view(doc_type='office',
                                      local_name='office',
                                      default_template='offices/_single.html',),
            name='detail')],
        namespace='offices')),

    url(r'^sub-pages/', include([
        url(r'^(?P<doc_id>[\w-]+)/$',
            SheerTemplateView.as_view(doc_type='sub_page',
                                      local_name='sub_page',
                                      default_template='sub-pages/_single.html'),
            name='detail')],
        namespace='sub_page')),

    url(r'^activity-log/$',
        TemplateView.as_view(template_name='activity-log/index.html'),
        name='activity-log'),

    url(r'^subscriptions/new/$',
        'core.views.govdelivery_subscribe',
        name='govdelivery'),

    url(r'^govdelivery-subscribe/', include([
        url(r'^success/$',
            TemplateView.as_view(
                template_name='govdelivery-subscribe/success/index.html'),
            name='success'),
        url(r'^error/$',
            TemplateView.as_view(
                template_name='govdelivery-subscribe/error/index.html'),
            name='user_error'),
        url(r'^server-error/$',
            TemplateView.as_view(
                template_name='govdelivery-subscribe/server-error/index.html'),
            name='server_error')],
        namespace='govdelivery')),

    url(r'^feed/(?P<doc_type>[\w-]+)/$', SheerlikeFeed(), name='feed'),

    url(r'^about-us/$', SheerTemplateView.as_view(template_name='about-us/index.html'), name='about-us'),

    url(r'^careers/', include([
        url(r'^$', TemplateView.as_view(template_name='careers/index.html'),
            name='careers'),

        url(r'^(?P<doc_id>[\w-]+)/$',
            SheerTemplateView.as_view(doc_type='careers',
                                      local_name='careers',
                                      default_template='careers/_single.html'), name='career'),

        url(r'^current-openings/$', SheerTemplateView.as_view(template_name='current-openings/index.html'),
            name='current-openings'),
        url(r'^students-and-graduates/$', SheerTemplateView.as_view(template_name='students-and-graduates/index.html'),
            name='students-and-graduates'),

        url(r'^working-at-cfpb/$', SheerTemplateView.as_view(template_name='working-at-cfpb/index.html'),
            name='working-at-cfpb'),

    ],
        namespace='careers')),

    url(r'^transcripts/', include([
        url(r'^how-to-apply-for-a-federal-job-with-the-cfpb/$', SheerTemplateView.as_view(
            template_name='transcripts/how-to-apply-for-a-federal-job-with-the-cfpb/index.html'),
            name='how-to-apply-for-a-federal-job-with-the-cfpb'),
    ],
        namespace='transcripts')),

    url(r'', include(wagtail_urls)),
]

from sheerlike import register_permalink

register_permalink('posts', 'blog:detail')
register_permalink('newsroom', 'newsroom:detail')
register_permalink('office', 'offices:detail')
register_permalink('sub_page', 'sub_page:detail')
register_permalink('events', 'events:event')
register_permalink('career', 'careers:career')
