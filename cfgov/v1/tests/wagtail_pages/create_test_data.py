# This is a standalone file. Running it will create wagtail pages
# This data allows integration tests to pass
# To run this file locally, run the following commands on a bash shell within
# the python container from the root folder:
#
# ./cfgov/manage.py shell
# exec(open('/src/consumerfinance.gov/cfgov/v1/tests/wagtail_pages/create_test_data.py').read())

# imports here. To import "create a page" functions, import from 
# v1.tests.wagtail_pages.helpers

# functions here. "create a page" functions return a path to the created page 
# or None if no page was created

# when adding tags or categories, make sure you pass them in a set:
# MY_TAGS = {"a tag", "another tag"}

# the first three arguments of any "create a page" function are title, slug,
# and parent path (optional, defaults to root)

# to create a menu or other wagtail object, the preferred method is to use
# json.dumps()

# call functions here