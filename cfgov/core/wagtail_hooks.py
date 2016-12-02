from urllib import quote, urlencode
from wagtail.wagtailcore import hooks

from core.utils import signed_redirect


@hooks.register('cfgovpage_context_handlers')
def signed_share_links(page, request,  context, *args, **kwargs):
    quoted_url = quote(page.url)
    page_info = dict(title=page.seo_title, url=quoted_url)
    context['mail_url'] = "mailto:?subject={title}&amp;body=Check out this page from the CFPB - {url}".format(**page_info)
    facebook_base_url = 'https://www.facebook.com/dialog/share'
    facebook_url_args = {'app_id': '210516218981921',
                         'display': 'page',
                         'href': page.url,
                         'redirect_url': page.url,
                         }
    facebook_share_url = "{0}?{1}".format(facebook_base_url, urlencode(facebook_url_args))
    context['facebook_url'] = signed_redirect(facebook_share_url)

    twitter_base_url = 'http://twitter.com/intent/tweet'
    twitter_url_args = {'url': page.url,
                        'via': 'CFPB',
                        'related': 'cfpb',
                        'text': (page.seo_title or \
                        "Look what I found on the CFPB's site!") +
                        " --"}

    twitter_share_url = "{0}?{1}".format(twitter_base_url, urlencode(twitter_url_args))
    context['twitter_url']= signed_redirect(twitter_share_url)

    linkedin_base_url = 'https://www.linkedin.com/shareArticle'
    linkedin_url_args = {'mini': 'true',
                         'url': page.url,
                         'title':page.title
                         }

    linkedin_share_url = "{0}?{1}".format(linkedin_base_url, urlencode(linkedin_url_args))
    context['linkedin_url'] = signed_redirect(linkedin_share_url)
