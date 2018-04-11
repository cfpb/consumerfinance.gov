## Development tips

### TIP: Developing on nested satellite apps
Some projects can sit inside cfgov-refresh, but manage their own asset
dependencies. These projects have their own package.json and base templates.

The structure looks like this:

#### npm modules
- App's own dependency list is in
  `cfgov/unprocessed/apps/[project namespace]/package.json`
- App's `node_modules` path is listed in the Travis config
  https://github.com/cfpb/cfgov-refresh/blob/master/.travis.yml#L10
  so that their dependencies will be available when Travis runs.

#### Webpack
- Apps may include their own webpack-config.js configuration that adjusts how
  their app-specific assets should be built. This configuration appears in
  `cfgov/unprocessed/apps/[project namespace]/webpack-config.js`

#### Templates
- Apps use a jinja template that extends the `base.html`
  template used by the rest of the site.
  This template would reside in `cfgov/jinja2/v1/[project namespace]/index.html`
  or similar (for example, [owning-a-home](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/jinja2/v1/owning-a-home/explore-rates/index.html)).

!!! note
    A template may support a non-standard browser, like an older IE version,
    by including the required dependencies, polyfills, etc. in its
    template's `{% block css %}` or `{% block javascript scoped %}` blocks.


### TIP: Loading satellite apps
Some projects fit within the cfgov-refresh architecture,
but are not fully incorporated into the project.
These are known as "satellite apps."

Satellite apps are listed in the
[optional-public.txt](https://github.com/cfpb/cfgov-refresh/blob/master/requirements/optional-public.txt)
requirements file.

In addition to the aforementioned list,
[HMDA Explorer](https://github.com/cfpb/hmda-explorer) and
[Rural or Underserved](https://github.com/cfpb/rural-or-underserved-test),
have their own installation requirements.

If using Docker, follow
[these guidelines](https://github.com/cfpb/cfgov-refresh/blob/master/docs/usage.md#develop-satellite-apps).

Otherwise, if not using Docker, follow these guidelines:

1. Build the third-party projects per their directions
1. Stop the web server and return to `cfgov-refresh`
1. Run `pip install -e ../<sibling>` to load the projects' dependencies

!!! note
    Do not install the projects directly into the `cfgov-refresh` directory.
    Clone and install the projects as siblings to `cfgov-refresh`,
    so that they share the same parent directory (`~/Projects` or similar).

### TIP: Loading data into Django models
The Django management command `import-data` will import data from the specified
source into the specified model.

```
usage: manage.py import-data [-h] [--version] [-v {0,1,2,3}] [--settings SETTINGS]
        [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--parent PARENT]
        [--snippet] -u USERNAME -p PASSWORD [--app APP] [--overwrite]
        data_type wagtail_type
```
- `data_type` is the WordPress post type defined in the `processors.py` file.
- `wagtail_type` is the Django model name where the data is going to go.
- `-u` and `-p` are credentials to an admin account.

Required option:

- `--parent` is the slug of the parent page that the pages will exist
  under.
- `--snippet` is a flag that's used to signify that the importing data will be
  inserted into a Django model, registered as a [Wagtail snippet](http://docs.wagtail.io/en/v2.0.1/topics/snippets.html).
  One of these options must be set for the command to run.

Other options:

- `--app` is the name of the app the Django models from `wagtail_type` exist in.
  It defaults to our app, `v1`.
- `--overwrite` overwrites existing pages in Wagtail based on comparing slugs.
Be careful when using this as it will overwrite the data in Wagtail with data
from the source. Default is `False`.
- `--verbosity` is set to 1 by default. Set it to 2 or higher and expect the
name of the slugs to appear where appropriate.

For now, in order for this command to import the data, one of the things it
needs is a file for "sheer logic" to use to retrieve the data. For us, the
processors are already done from our last backend. This part of the command
will change as we move away from our dependency on "sheer logic." This is set
by putting the file in a `processors` module in the top level of the project
and adding it to the setting [`SHEER_PROCESSORS`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/cfgov/settings/base.py#L218).

The command needs a `processors` module in the app that's passed to it, as well
as a file with the same name as the Django model specified that defines a class
named `DataConverter` that subclasses either `_helpers.PageDataConverter` or
`_helpers.SnippetDataConverter` and implements their method(s) explained below:

**PageDataConverter**:

 - **convert(self, imported_data)**:
   For converting pages or snippets, the processor file must implement the
   **convert()** function with one argument. That argument represents the
   imported data dictionary. That function must take the dictionary and map it
   to a new one that uses the keys that Wagtail's **create()** and **edit()**
   admin/snippet view functions expect in the `request.POST` dictionary to
   actually migrate the data over, and then returns that dictionary where it
   will be assigned to `request.POST`.

**SnippetDataConverter(PageDataConverter)**:

 - **get_existing_snippet()**
   This also accepts the imported data dictionary. It's used to find an
   existing snippet given the imported data, returning it if found or `None` if
   not.

### TIP: Working with the templates

#### Front-End Template/Asset Locations

**Templates** that are served by the Django server: `cfgov\jinja2\v1`

**Static assets** prior to processing (minifying etc.): `cfgov\unprocessed`.

!!! note
    After running `gulp build` the site's assets are copied over to `cfgov\static_built`,
    ready to be served by Django.

#### Simple static template setup

By default, Django will render pages with accordance to the URL pattern defined
for it. For example, going to `http://localhost:8000/the-bureau/index.html`
(or `http://localhost:8000/the-bureau/`) renders `/the-bureau/index.html` from
the `cfgov` app folder's `jinja2/v1` templates folder as processed
by the [Jinja2](http://jinja.pocoo.org/docs) templating engine.

### TIP: Outputting indexed content in a Sheer template

Most of our content is indexed from the API output of our WordPress back-end.
This happens when the `python cfgov/manage.py sheer_index -r` command is run.

There are two ways in which we use indexed content:
repeating items (e.g., blog posts and press releases),
and single pages (e.g., the Future Requests page in Doing Business with Us).
What follows is a deeper dive into both of these content types.

#### Single content

To access a single piece of content,
the easiest thing to do is use the `get_document()` function.

Using the example given earlier of the Future Requests page,
here's how it's done:

```jinja
{% set page = get_document('pages', '63169') %}
{{ page.content | safe }}
```

The `get_document` method can be used to retrieve a single item of any post type
for display within a template.
In the below example we get an instance of the non-hierarchical
`contact` post type using its slug (`whistleblowers`):

```jinja
{% set whistleblowers = get_document('contact', 'whistleblowers') %}
```

In practice, many of our templates are a Frankenstein-type mixture
of hand-coded static content and calls to indexed content,
as we continually try to strike the right balance of what content
is appropriate to be edited by non-developers in Wagtail,
and what is just too fragile to do any other way than by hand.

### TIP: Filtering results with queries

Sometimes you'll want to create queries in your templates to filter the data.

The two main ways of injecting filters into your data are in the URL's query
string and within the template code itself.

We have a handy function `search()` that:

1. Pulls in filters from the URL query string.
2. Allows you to add additional filters by passing them in as arguments to the function.

#### URL query string filters

URL query string filters can be further broken down into two types:

1. Term - Used when you want to filter by whether a field matches a term.
Note that in order to use this type of filter,
the field you are matching it against must have
`"index": "not_analyzed"` set in the mapping.
2. Range - Used for when you want to filter something by a range (e.g. dates or numbers)

An example of Term is:

`?filter_category=Op-Ed`

`filter_[field]=[value]`

An example of Range is:

`?filter_range_date_gte=2014-01`

`filter_range_[field]_[operator]=[value]`

URL query string filters are convenient for many of the filtered queries you'll need to run,
but often there are cases where you'll need more flexibility.

#### More complex filters

By default, `search()` uses the default query parameters
defined in the `_queries/object-name.json` file,
then mixes them in with any additional arguments
from the URL query string in addition to what is passed into the function itself.

When using `search()`, you can also pass in filters with the same `filter_` syntax as above.

For example:

`search(filter_category='Op-Ed')`

Multiple term filters on the same field will be combined in an OR clause, while
term filters of different fields will be combined in an AND clause.

For example:

`search(filter_tag='Students', filter_tag='Finance', filter_author='Batman')`

This will return documents that have the tag Students OR Finance, AND have an author of Batman.

If you need more control over your filter than that,
enter it manually in the `cfgov/jinja2/v1/_queries/[filtername].json` file.

### TIP: Debugging site performance

When running locally it is possible to enable the
[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/stable/)
by defining the `ENABLE_DEBUG_TOOLBAR` environment variable:

```sh
$ ENABLE_DEBUG_TOOLBAR=1 ./runserver.sh
```

This tool exposes various useful pieces of information about things like HTTP headers,
Django settings, SQL queries, and template variables. Note that running with the toolbar on
may have an impact on local server performance.

### TIP: Updating the documentation

Our documentation is written as Markdown files and served in GitHub pages
by [mkdocs](https://www.mkdocs.org/user-guide/deploying-your-docs/).

To update the docs in GitHub Pages once a pull request has been merged,
mkdocs provides [a helpful command](https://www.mkdocs.org/user-guide/deploying-your-docs/):

```
mkdocs gh-deploy --clean
```
