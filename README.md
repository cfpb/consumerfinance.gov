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
`grunt vendor`, then run `grunt` to rebuild everything:

```bash
$ npm install
$ grunt vendor
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

### Filtering results with queries

Sometimes you'll want to create queries in your templates to filter the data.

The two main ways of injecting filters into your data are in the URL's query string and within the template code itself.

We have a handy function `search_with_url_arguments()` that:

1. Pulls in filters from the URL query string
2. Allows you to add additional filters by passing them in as arguments to the function

#### URL query string filters

URL query string filters can be further broken down into two types:

1. Bool - Used when you want to filter by whether a field matches a keyword, is True or False, etc.
2. Range - Used for when you want to filter something by a range (e.g. dates or numbers)

An example of Bool is:

?filter_category=Op-Ed

`filter_[field]=[value]`

When you go to a URL such as http://localhost:7000/blog/?filter_category=Op-Ed and you use `search_with_url_arguments()`, the queryset returned will only include objects with a category of 'Op-Ed'.

An example of Range is:

?filter_range_date_gte=2014-01

filter_range_[field]_[operator]=[value]

Continuing with the example above, if you go to a URL such as http://localhost:7000/blog/?filter_range_date_gte=2014-01 and you use `search_with_url_arguments()`, you'll get a queryset of objects where the 'date' field is in January, 2014 or later.

URL query string filters are convenient for many of the filtered queries you'll need to run, but often there are cases where you'll need more flexibility.

#### More complex filters

By default, `search_with_url_arguments()` uses the default query parameters defined in the _queries/object-name.json file, then mixes them in with any additional arguments from the URL query string in addition to what is passed into the function itself.

The list of available arguments are outlined in elasticsearch-py's [search method](http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch.Elasticsearch.search)

The most common ones we use are size (to change the number of results returned) and q (to query based on specific fields).

When using q, you'll need to use the [Lucene Query Parser Syntax](http://lucene.apache.org/core/2_9_4/queryparsersyntax.html)

Here is an example of using q: 

```
{% set events_jan2014 = queries.calendar_event.search_with_url_arguments(q="dtstart:[2014-01-01 TO 2014-01-31]") %}
```

This will return a queryset of calendar_event objects which, for the field 'dtstart', have a date in January, 2014.
