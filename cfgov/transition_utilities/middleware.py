def alter_content(content):
    return content.replace('/wp-content/themes/cfpb_nemo/', '/static/nemo/')

class RewriteNemoURLsMiddleware(object):
    def process_response(self,request,response):
        if response.streaming:
            response.streaming_content = wrap_streaming_content(response.streaming_content)
        else:
            response.content = alter_content(response.content)

        return response
