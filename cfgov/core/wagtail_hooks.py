from wagtail.wagtailcore import hooks

from core.utils import signed_redirect, append_query_args_to_url


@hooks.register('cfgovpage_context_handlers')
def signed_share_links(page, request,  context, *args, **kwargs):

    mail_args = {'title': page.seo_title,
                 'url': page.url,
                 }

    # the 'append_query_args_to_url' approach doesn't seem to play well with
    # email (the resulting subject line and body will be URL+encoded when
    # they appear in the users mail client), so string formatting it is.
    context['mail_url'] = "mailto:?subject={title}&amp;body=Check out this page from the CFPB - {url}".format(**mail_args)

    facebook_base_url = 'https://www.facebook.com/dialog/share'
    facebook_url_args = {'app_id': '210516218981921',
                         'display': 'page',
                         'href': page.url,
                         'redirect_url': page.url,
                         }
    facebook_share_url = append_query_args_to_url(facebook_base_url,
                                                  facebook_url_args)

    context['facebook_url'] = signed_redirect(facebook_share_url)

    twitter_base_url = 'http://twitter.com/intent/tweet'
    twitter_url_args = {'url': page.url,
                        'via': 'CFPB',
                        'related': 'cfpb',
                        'text': (page.seo_title or
                                 "Look what I found on the CFPB's site!") +
                        " --"}

    twitter_share_url = append_query_args_to_url(twitter_base_url,
                                                 twitter_url_args)

    context['twitter_url'] = signed_redirect(twitter_share_url)

    linkedin_base_url = 'https://www.linkedin.com/shareArticle'
    linkedin_url_args = {'mini': 'true',
                         'url': page.url,
                         'title': page.title
                         }

    linkedin_share_url = append_query_args_to_url(linkedin_base_url,
                                                  linkedin_url_args)

    context['linkedin_url'] = signed_redirect(linkedin_share_url)
