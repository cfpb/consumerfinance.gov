## Development tips

### TIP: Updating npm shrinkwrapped dependencies
For [security reasons](http://www.infoworld.com/article/3048526/security/nodejs-alert-google-engineer-finds-flaw-in-npm-scripts.html),
the dependencies in [`package.json`](/package.json) are pinned to a version
in [`npm-shrinkwrap.json`](/npm-shrinkwrap.json).
This means updating a project dependency requires updating both files.
The easiest way to do this is the following steps:

 1. Update the version of the dependency in `package.json`.
 2. Delete the `node_modules` directory.
 3. Delete the `npm-shrinkwrap.json` file.
 4. Run `npm install`.
 5. Run `npm shrinkwrap --dev`.

Congrats! The dependency has been updated.

### TIP: Loading sibling projects
Some projects fit within the cfgov-refresh architecture,
but are not fully incorporated into the project.
These are known as "non-v1 Django apps."
In order to visit areas of the site locally where those projects are used,
the sibling projects need to be installed
and then indexed within this cfgov-refresh project.

The non-v1 apps are the following:

 - [Owning a Home](https://github.com/cfpb/owning-a-home).
 - fin-ed-resources (ghe/CFGOV/fin-ed-resources) - for the Education Resources section.
 - know-before-you-owe (ghe/CFGOV/know-before-you-owe) - for the Consumer Tools > Know before you owe section.

After installing these projects as sibling directories to the `cfgov-refresh` repository,
build the third-party projects per their directions,
stop the web server and return to `cfgov-refresh`
and run `cfgov/manage.py sheer_index -r` to load the projects' data into ElasticSearch.

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
  inserted into a Django model, registered as a [Wagtail snippet](http://docs.wagtail.io/en/v1.1/topics/snippets.html).
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

#### Repeating content

For any kind of repeating content, this is the basic process:

1. In the vars file for the section you're in (e.g., `newsroom/_vars-newsroom.html`),
   we set up a variable that holds the results of the default query we want to run.

   Here's how it looks for the blog:

```jinja
{% set query = queries.posts %}
{% set posts = query.search(size=10) %}
```


2. If you want to display the repeating content within a template,
   simply set up a `for ... in` loop,
   then output the different properties of the post within.
   In the case of the blog, a list of posts is built using this method in
   `cfgov/jinja2/v1/_includes/posts-paginated.html`.

   Here is a simplified example:

```jinja
{% for post in posts %}
  <h1>{{ post.title }}</h1>
  {{ post.content }}
{% endfor %}
```

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

### TIP: Updating the documentation

Our documentation is written as Markdown files and served in GitHub pages 
by [mkdocs](http://www.mkdocs.org/user-guide/deploying-your-docs/).

To update the docs in GitHub Pages once a pull request has been merged, 
mkdocs provides [a helpful command](http://www.mkdocs.org/user-guide/deploying-your-docs/):

```
mkdocs gh-deploy --clean
```
