# cfgov-refresh

Layout and content for the consumerfinance.gov Refresh project.

### This project is a work in progress

Nothing presented in the issues or in this repo is a final product
unless it is marked as such or appears on www.consumerfinance.gov.


## Contributing

We welcome your feedback and contributions.

- [Find out about contributing](https://cfpb.github.io/capital-framework/contributing/)
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
