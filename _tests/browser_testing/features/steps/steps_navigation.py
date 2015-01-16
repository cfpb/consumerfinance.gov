from behave import given

# RELATIVE URLs
NEWSROOM = 'newsroom'

@given(u'I navigate to the "{page_name}" page')
def step(context, page_name):
    if page_name == 'Newsroom':
        context.base.go(NEWSROOM)
    else:
        raise Exception(page_name + ' is NOT a valid page')