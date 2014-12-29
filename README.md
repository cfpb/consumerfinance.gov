# cfgov-refresh

Layout and content for the consumerfinance.gov Refresh project.

### This project is a work in progress

Nothing presented in the issues or in this repo is a final product
unless it is marked as such or appears on www.consumerfinance.gov.


## Contributing

We welcome your feedback and contributions.

- [Find out about contributing](https://cfpb.github.io/capital-framework/contributing/)
  _More specific cfgov-refresh contributing guidelines are coming soon._
- [File a bug](https://github.com/cfpb/cfgov-refresh/issues/new?body=%23%23%20URL%0D%0D%0D%23%23%20Actual%20Behavior%0D%0D%0D%23%23%20Expected%20Behavior%0D%0D%0D%23%23%20Steps%20to%20Reproduce%0D%0D%0D%23%23%20Screenshot&labels=bug)


## Getting started

### Requirements

- [Sheer](https://github.com/cfpb/sheer)
- [elasticsearch](http://www.elasticsearch.org/)
- [Node](http://nodejs.org/)
- [Grunt](http://gruntjs.com/)
- [Bower](http://bower.io/)

### Back end setup

Set up [Sheer](https://github.com/cfpb/sheer#installation),
a Jekyll-inspired, elasticsearch-powered, CMS-less publishing tool.

#### Additional setup requirements for this site

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

_You can also add the `export` line to your `.bash_profile`,
or use your favorite alternative method of setting environment variables._

### Front end setup

The cfgov-refresh front end currently uses the following:

- [Less](http://lesscss.org/)
- [Capital Framework](https://cfpb.github.io/capital-framework/)
- [Grunt](http://gruntjs.com/)
- [Bower](http://bower.io/) & [npm](https://www.npmjs.org/) for package management

If you're new to Capital Framework, we encourage you to
[start here](https://cfpb.github.io/capital-framework/).

#### Installing dependencies (one time)

1. Install [node.js](http://nodejs.org/) however you'd like.
2. Install [Grunt](http://gruntjs.com/), [Bower](http://bower.io/),
   and [Browserify](http://browserify.org/):

```
$ npm install -g grunt-cli bower browserify
```

### Developing

Each time you fetch from upstream, install dependencies with npm and
run `grunt` to build everything:

```bash
$ npm install
$ grunt
```

To work on the app you will need sheer running to compile the templates.
There is also a `grunt watch` command that will recompile Less and JS
on the fly while you're developing.

```bash
# use the sheer virtualenv
$ workon sheer

# index the latest content
$ sheer index

# start sheer
$ sheer serve --debug

# open a new command prompt and run:
$ grunt watch
```

To view the site browse to: <http://localhost:7000/>

To view the project layout docs and pattern library,
go to <http://localhost:7000/docs/>


## Tests

To run browser tests, you'll need to perform the following steps:

1. Install chromedriver: 
  - Mac: `brew install chromedriver`
  - Manual (Linux/Mac): Download the latest
    [Chromedriver](http://chromedriver.storage.googleapis.com/index.html)
    binary and put it somehwere on your path (e.g. /path/to/your/venv/bin)
2. `pip install -r _tests/requirements.txt`
3. `nosetests -v _tests`


## How this repo is versioned

We use an adaptation of [Semantic Versioning 2.0.0](http://semver.org).
Given the `MAJOR.MINOR.PATCH` pattern, here is how we decide to increment:

- The MAJOR number will be incremented for major redesigns that require the user
  to relearn how to accomplish tasks on the site.
- The MINOR number will be incremented when new content or features are added.
- The PATCH number will be incremented for all other changes that do not rise
  to the level of a MAJOR or MINOR update.
