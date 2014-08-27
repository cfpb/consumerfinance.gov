# cfgov-refresh

cfgov-refresh is based off of [cf-demo](),
a the recommended workflow for using Capital Framework components.

If you're new to Capital Framework, we encourage you to
[start here](http://cfpb.github.io/capital-framework/).

- [View the docs](http://cfpb.github.io/cfgov-refresh/docs/)
- [See the demos](http://cfpb.github.io/cfgov-refresh/)


## Contributing

We welcome your feedback and contributions.

- [Find out about contributing](http://cfpb.github.io/capital-framework/contributing/)
  _More specific cfgov-refresh contributing guidelines are coming soon._
- [File a bug](https://github.com/cfpb/cfgov-refresh/issues/new?body=%23%23%20URL%0D%0D%0D%23%23%20Actual%20Behavior%0D%0D%0D%23%23%20Expected%20Behavior%0D%0D%0D%23%23%20Steps%20to%20Reproduce%0D%0D%0D%23%23%20Screenshot&labels=bug)


## Getting started

### Back end

Set up [Sheer](https://github.com/cfpb/sheer),
a Jekyll-inspired, elasticsearch-powered, CMS-less publishing tool.

###$ Additional setup requirements for this site

Install these dependencies:

```sh
pip install git+git://github.com/dpford/flask-govdelivery
pip install git+git://github.com/rosskarchner/govdelivery
```

_We are working on a way to get these installed automatically._

And ask someone for the values to set the following environment variables:

- `GOVDELIVERY_BASE_URL`
- `GOVDELIVERY_ACCOUNT_CODE`
- `GOVDELIVERY_USER`
- `GOVDELIVERY_PASSWORD`
- `SUBSCRIPTION_SUCCESS_URL`
- `WORDPRESS`

#### Run Sheer

  - `sheer index`
  - `sheer serve`

_You can also add the `export` line to your `.bash_profile`,
or use your favorite alternative method of setting environment variables._

### Front end

Since cfgov-refresh is based off of cf-demo we encourage you to start with the
[cf-demo docs](http://cfpb.github.io/capital-framework/cf-demo/).
_More specific cfgov-refresh docs are coming soon._


## How this repo is versioned

We use an adaptation of [Semantic Versioning 2.0.0](http://semver.org).
Given the `MAJOR.MINOR.PATCH` pattern, here is how we decide to increment:

- The MAJOR number will be incremented for major redesigns that require the user
  to relearn how to accomplish tasks on the site.
- The MINOR number will be incremented when new content or features are added.
- The PATCH number will be incremented for all other changes that do not rise
  to the level of a MAJOR or MINOR update.
