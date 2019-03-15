from django.template.response import SimpleTemplateResponse


# Remove this file after the HMDA API is retired and the
# Legacy HMDA Explorer page is no longer needed.
def legacy_explorer_view(request):
    response = SimpleTemplateResponse('orange-explorer.html')
    return response.render()
