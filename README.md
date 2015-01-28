# cfgov-refresh

This repository contains the redesign-in-progress of consumerfinance.gov. This includes front-end assets and build tools, and configuration for [Sheer](https://github.com/cfpb/sheer) to load content from Wordpress and Django back-ends to elasticsearch to render the site.

### This project is a work in progress

Nothing presented in the issues or in this repo is a final product
unless it is marked as such or appears on www.consumerfinance.gov.


## Contributing

We welcome your feedback and contributions.

- [Find out about contributing](https://cfpb.github.io/capital-framework/contributing/)
- [File a bug](https://github.com/cfpb/cfgov-refresh/issues/new?body=%23%23%20URL%0D%0D%0D%23%23%20Actual%20Behavior%0D%0D%0D%23%23%20Expected%20Behavior%0D%0D%0D%23%23%20Steps%20to%20Reproduce%0D%0D%0D%23%23%20Screenshot&labels=bug)


## Getting started

### Requirements

##### Back-end
- [Sheer](https://github.com/cfpb/sheer)
- [elasticsearch](http://www.elasticsearch.org/)

##### Front-end Build Tools
- [Node](http://nodejs.org/) and NPM

### Back end setup

Set up [Sheer](https://github.com/cfpb/sheer#installation),
a Jekyll-inspired, elasticsearch-powered, CMS-less publishing tool.

#### Additional setup requirements for this site

Install these dependencies into your virtual environment (we called ours 'sheer'):

```sh
workon sheer

pip install git+git://github.com/dpford/flask-govdelivery
pip install git+git://github.com/rosskarchner/govdelivery
```

_We are working on a way to get these installed automatically._

And ask someone for the values to set the following environment variables:

- `WORDPRESS`(url to WordPress install)
- `GOVDELIVERY_BASE_URL`
- `GOVDELIVERY_ACCOUNT_CODE` (GovDelivery account variable)
- `GOVDELIVERY_USER` (GovDelivery account variable)
- `GOVDELIVERY_PASSWORD` (GovDelivery account variable)
- `SUBSCRIPTION_SUCCESS_URL` (Forwarding location on Subscription Success)

_You can also `export` the above environment variables to your `.bash_profile`,
or use your favorite alternative method of setting environment variables._

__NOTE__ about GovDelivery: GovDelivery is a third party web service that powers our subscription forms. Users may decide to swap this tool out for another third party service. The application will function but throw an error if the above GovDelivery values are not set. 

### Front end setup

The cfgov-refresh front end currently uses the following frameworks / tools:

- [Grunt](http://gruntjs.com/)
- [Bower](http://bower.io/)
- [Less](http://lesscss.org/)
- [Capital Framework](http://cfpb.github.io/capital-framework/getting-started/)


If you're new to Capital Framework, we encourage you to
[start here](http://cfpb.github.io/capital-framework/getting-started/).

#### Installing dependencies (one time)

1. Install [node.js](http://nodejs.org/) however you'd like.
2. Install [Grunt](http://gruntjs.com/) and [Bower](http://bower.io/):
3. 
```
$ npm install -g grunt-cli bower
```

### Developing

Each time you fetch from upstream, you should install dependencies with npm and
`grunt vendor`, then run `grunt` to rebuild everything:

```bash
$ npm install
$ grunt vendor
$ grunt
```

To work on the app you will need sheer running to compile the templates.
There is also a `grunt watch` command that will recompile Less and JS
on the fly while you're developing. To do this, run the following:

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


## Working with the templates

### Simple static template setup

By default, Sheer will render pages at their natural paths in the project's file
structure.
For example, going to <http://localhost:7000/the-bureau/index.html>
(or <http://localhost:7000/the-bureau/>) renders `/the-bureau/index.html`
as processed by the [Jinja2](http://jinja.pocoo.org/docs/) templating engine.
Note that this page does not automatically show any content indexed by Sheer;
it simply outputs the static HTML written into the template.

### Outputting indexed content in a Sheer template

Most of our content is indexed from the API output of our WordPress back end.
(We used to use WordPress to serve the front end of the site,
but going forward, it will simply be a content editing and storage system.)
This happens when the `sheer index` command is run.

If your content isn't being indexed yet, see "Setting up a new WordPress post
type and processing it with Sheer" on the flapjack/Getting-started-with-Flapjack
wiki (on our GitHub Enterprise server).

There are two ways in which we use indexed content: repeating items
(e.g., blog posts and press releases), and single pages
(e.g., the Future Requests page in Doing Business with Us).

#### Repeating content

For any kind of repeating content, this is the basic process:

1. In the vars file for the section you're in (e.g., `blog/_vars-blog.html`), we
   set up a variable that holds the results of the default query we want to run.

   Here's how it looks for the blog:

   ```jinja
   {% set query = queries.posts %}
   {% set posts = query.search_with_url_arguments(size=10) %}
   ```
2. If you want to display the repeating content within a template, simply set up
   a `for ... in` loop, then output the different properties of the post within.
   In the case of the blog, a list of posts is built using this method in
   `_layouts/posts-paginated.html`.

   Here is a simplified example:

   ```jinja
   {% for post in posts %}
     <h1>{{ post.title }}</h1>
     {{ post.content }}
   {% endfor %}
   ```
3. If you would like to display each instance of repeating content in a separate
   page, create a `_single.html` template (in the case of the blog, located at
   `blog/_single.html`) and a corresponding entry in `_settings/lookups.json`.
   Sheer will automatically create URLs for every post of that type and render
   them with the `_single.html` template.
   This is how separate pages are generated for each blog post.

#### Single content

To access a single piece of content, the easiest thing to do is use the
`get_document()` function.

Using the example given earlier of the Future Requests page, here's how it's
done:

```jinja
{% set page = get_document('pages', '63169') %}
{{ page.content | safe }}
```

This example pulls a WordPress page into a template.
We use the page post type (i.e., the built-in "Page" entries in WordPress)
when all or most of a page's content can be edited in WordPress.

Note that when accessing a WordPress page, you must use the numeric ID to
identify the page you want to get, as multiple pages can have the same slug.
(This is also true of any custom post type that is hierarchical.)

The `get_document` method can be used to retrieve a single item of any post type
for display within a template.
In this example from `contact-us/promoted-contacts.html`, we get an instance of
the non-hierarchical `contact` post type using its slug (`whistleblowers`):

```jinja
{% set whistleblowers = get_document('contact', 'whistleblowers') %}
```

In practice, many of our templates are a Frankenstein-type mixture of hand-coded
static content and calls to indexed content, as we continually try to strike the
right balance of what content is appropriate to be edited by non-developers in
WordPress, and what is just too fragile to do any other way than by hand.

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

The list of available arguments are outlined in elasticsearch-py's [search method](http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch.Elasticsearch.search).

The most common ones we use are size (to change the number of results returned) and q (to query based on specific fields).

When using q, you'll need to use the [Lucene Query Parser Syntax](http://lucene.apache.org/core/2_9_4/queryparsersyntax.html).

Here is an example of using q: 

```
{% set events_jan2014 = queries.calendar_event.search_with_url_arguments(q="dtstart:[2014-01-01 TO 2014-01-31]") %}
```

This will return a queryset of calendar_event objects which, for the field 'dtstart', have a date in January, 2014.

## Tests

To run browser tests, you'll need to perform the following steps:

1. Install chromedriver: 
  - Mac: `brew install chromedriver`
  - Manual (Linux/Mac): Download the latest
    [Chromedriver](http://chromedriver.storage.googleapis.com/index.html)
    binary and put it somehwere on your path (e.g. /path/to/your/venv/bin)
2. In _tests/browser_testing/features/, copy example-environment.cfg to environment.cfg and change the `chrome_driver` path to the proper path for your webdriver binary.  If you installed via homebrew, this will be /path/to/homebrew/bin/chromedriver.
3. `pip install -r _tests/browser_testing/requirements.txt`
4. `cd _tests/browser_testing/`
5. Start the tests: `behave`


## How this repo is versioned

We use an adaptation of [Semantic Versioning 2.0.0](http://semver.org).
Given the `MAJOR.MINOR.PATCH` pattern, here is how we decide to increment:

- The MAJOR number will be incremented for major redesigns that require the user
  to relearn how to accomplish tasks on the site.
- The MINOR number will be incremented when new content or features are added.
- The PATCH number will be incremented for all other changes that do not rise
  to the level of a MAJOR or MINOR update.
