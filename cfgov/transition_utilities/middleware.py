from django.conf import settings

def alter_content(content):
    content = content.replace('http://www.consumerfinance.gov/wp-content/themes/cfpb_nemo/',
            '/static/nemo/')
    if settings.DEBUG:
        content = content.replace('fakes3/bucket', 'localhost:4569/fakes3/bucket')
    return content.replace('/wp-content/themes/cfpb_nemo/', '/static/nemo/')

def wrap_streaming_content(content):
    for chunk in content:
        yield alter_content(chunk)

class RewriteNemoURLsMiddleware(object):
    def process_response(self,request,response):
        if response.streaming:
            response.streaming_content = wrap_streaming_content(response.streaming_content)
        else:
            response.content = alter_content(response.content)

        return response
