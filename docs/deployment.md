# Deployment

This project tries to follow standard Django and Wagtail conventions and
therefore should be compatible with a variety of deployment methods.

See 
[Deploying Django](https://docs.djangoproject.com/en/1.11/howto/deployment/)
and
[Deploying Wagtail](https://docs.wagtail.io/en/v1.13.4/advanced_topics/deploying.html)
for some external documentation of different approaches.

## Drama-free Django

We use a tool named
[drama-free-django](https://github.com/cfpb/drama-free-django)
to build deployable artifacts for consumerfinance.gov.
Existing documentation for that project can be found in its source code repository.

The automated [Travis CI checks](../travis/) for cfgov-refresh invoke
drama-free-django to test generating and installing a deploy artifact.
