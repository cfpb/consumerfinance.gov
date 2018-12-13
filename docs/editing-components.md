# Creating and Editing Wagtail Components

cfgov-refresh implements a number of components
that editors can choose from when building a page,
for example: Heroes, Expandable Groups, or Info Unit Groups.
In Wagtail parlance, these are called
["StreamField blocks"](https://docs.wagtail.io/en/v1.13.4/topics/streamfield.html)*
(or just "blocks").
We sometimes also refer to them as "modules", because we think that
the terms "component" and "module" may be more obvious to non-developers.
This page will use the terms somewhat interchangeably.
One other important thing to note before we begin:
blocks can be nested within other blocks.

_* If you're going to be doing anything more than making minor updates to
   existing components, this is highly recommended reading._




## Table of contents

1. [The parts of a Wagtail block](#the-parts-of-a-wagtail-block)
   1. [The back end](#the-back-end)
      1. [The Python class](#the-python-class)
      1. [Adding it to a StreamField](#adding-it-to-a-streamfield)
   1. [The front end](#the-front-end)
      1. [The HTML template](#the-html-template)
      1. [Adding some style](#adding-some-style)
      1. [Adding some JavaScript](#adding-some-javascript)
1. [How-to guides](#how-to-guides)
   1. [Adding a field](#adding-a-field)
   1. [Editing a field](#editing a field)
   1. [Removing a field](#removing-a-field)
   1. [Creating migrations for StreamField blocks](#creating-migrations-for-streamfield-blocks)




## The parts of a Wagtail block

Blocks are implemented via several different bits of code:

1. [Defining a block's fields and other properties in a Python class](#the-python-class)
1. [Adding the class to a page's StreamField block options](#adding-it-to-a-streamfield)
1. [Creating an HTML template for rendering the block on a page](#the-html-template)
1. [(Optionally) adding some Less for styling the block](#adding-some-style)
1. [(Optionally) adding some JavaScript for adding advanced behavior](#adding-some-javascript)

Before you dive in further,
[check out the Atomic Structure page](../atomic-structure/)
and familiarize yourself with our basic concepts
of atoms, molecules, and organisms.


### The back end

#### The Python class

A component's fields and other properties are defined in a Python class,
typically a subclass of Wagtail's
[`StructBlock`](http://docs.wagtail.io/en/v1.13.4/topics/streamfield.html#structblock).
These classes are located in a number of different files across the repository,
but there are two major categories they fall into:

1. Files corresponding to a general-purpose, site-wide atomic component.
   These files—`atoms.py`, `molecules.py`, and `organisms.py`—are located in
   [`cfgov/v1/atomic_elements`](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements).
2. Files that are specific to a particular sub-app, such as regulations3k's
   [blocks.py](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/regulations3k/blocks.py).

There are other places where StreamField block classes are defined
(particularly blocks that are only ever used as fields within another block),
but these are the two most common locations
where top-level Wagtail modules are stored.

A simple component class looks like this:

```python
class RelatedContent(blocks.StructBlock):                      # 1
    heading = blocks.CharBlock(required=False)                 # 2
    paragraph = blocks.RichTextBlock(required=False)           # 3
    links = blocks.ListBlock(atoms.Hyperlink())                # 4

    class Meta:                                                # 5
        icon = 'grip'                                          # 6
        label = 'Related content'                              # 7
        template = '_includes/molecules/related-content.html'  # 8
```

There are a few things happening here:

1. The `RelatedContent` class is a subclass of
   [Wagtail's `StructBlock`](https://docs.wagtail.io/en/v1.13.4/topics/streamfield.html#structblock),
   which allows for the combination of a fixed number of other sub-blocks
   (see previous comment about blocks being nested within other blocks)
   into a single unit (what we'd think of as a "module" in the Wagtail editor).
   This one has three sub-blocks (lines 2, 3, and 4).
2. The `heading` field uses the basic Wagtail `CharBlock`, which results in a
   field with a basic single-line text input.
3. The `paragraph` field uses the basic Wagtail `RichTextBlock`,
   which results in a field with a multiline WYSIWYG text input.
4. The `links` field uses another basic Wagtail block, `ListBlock`,
   which is a special type of block that can hold a variable number of
   some other block (the `Hyperlink` atom block, in this case).
5. The `Meta` class defines some properties on the `RelatedContent` block
   that are used by the Wagtail admin or in rendering the block.
6. The `icon` property tells Wagtail what icon to use in the editor
   for the button you use to add a `RelatedContent` block to a StreamField.
   Icon options can be found in the Wagtail style guide when running locally:
   http://localhost:8000/admin/styleguide/#icons
7. The optional `label` property overrides the text of that same button;
   if `label` is not set, Wagtail will generate one from the name of the block.
8. The `template` property is a pointer to the HTML template used to render
   this component. [See below for more on templates.](#the-html-template)

This results in a module that looks like this in the Wagtail editor:

![A screenshot of a Related Content module with heading, paragraph, and links fields](img/related-content-module.png)

Note again that what we think of as **fields** are _also_ blocks,
and what we think of as **components** or **modules**
are a special kind of block, `StructBlock`,
that comprise the sub-blocks that are our fields.

There are two common optional things that are also used in component classes:

1. [Overriding the default `get_context` method](http://docs.wagtail.io/en/v1.13.4/topics/streamfield.html#streamfield-get-context)
   to pass additional data to the template
2. [Adding component-specific JavaScript](#adding-some-javascript)
    via the `Media` class

#### Adding it to a StreamField

Components are made available in the page editing interface
by adding them to one of a page types's StreamFields.
These are usually the first things in a page's class definition.
For example, see this snippet from `blog_page.py`:

```python
class BlogPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('email_signup', organisms.EmailSignUp()),
        ('feedback', v1_blocks.Feedback()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
    ])
    …
```

This sets up a StreamField named `content` that allows for
the insertion of any of those seven listed blocks into it.

To make the `RelatedContent` module (shown above) available to this StreamField,
we'd add a new entry to this list following the same format:
`('related_content', molecules.RelatedContent()),`.

Most page types have a couple StreamFields (`header` and `content`) in the
general content area (the first tab on an editing screen), and most also share
[a common `sidefoot` StreamField](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/base.py#L95-L107)
(so named for the fact that it appears on the right side on some page types,
but in the footer on others) on the sidebar tab.

---

!!! note "Don't forget the migrations!"
    Adding or changing fields on either Python class will always require a new
    [Django schema migration](https://docs.djangoproject.com/en/1.11/topics/migrations/);
    additionally, changing field names or types
    on an existing block will require a
    [Django data migration](https://docs.djangoproject.com/en/1.11/topics/migrations/#data-migrations).
    See the guide on
    [creating migrations for StreamField blocks](#creating-migrations-for-streamfield-blocks)
    for more details.


### The front end

#### The HTML template

As mentioned above, each module's Python class has a `Meta` class
that defines the location of its template file.
In the `RelatedContent` example,
it was `template = '_includes/molecules/related-content.html'`.
That path is relative to `cfgov/jinja2/v1/`.

This is what that template looks like (comments excluded):

```html
<div class="m-related-content">
    {% if value.heading %}
        <header class="m-slug-header">
            <h2 class="a-heading">
                {{ value.heading }}
            </h2>
        </header>
    {% endif %}

    {{ value.paragraph | safe }}

    {% if value.links %}
        <ul class="m-list m-list__links">
        {% for link in value.links %}
            <li class="m-list_item">
                <a href="{{ link.url }}" class="m-list_link">{{ link.text }}</a>
            </li>
        {% endfor %}
        </ul>
    {% endif %}
</div>
```

When Wagtail renders a block,
it includes the values of its fields in an object named `value`.
Above, you can see where the `heading` and `paragraph` fields are output with
[Jinja2 expression tags](http://jinja.pocoo.org/docs/2.10/templates/#expressions).
And note how the `links` field (a `ListBlock`) is iterated over,
and the values of _its_ `Hyperlink` child blocks are output.

That's about as simple an example as it gets, but block templates can get much
more complex when they have lots of child blocks and grandchild blocks.
Also, if a block definition has overridden `get_context` to pass other data
into the template (as described at the end of
[the Python class section](#the-python-class) above),
those context variables can also be output with simple Jinja2 expression tags:
`{{ context_var }}`.

#### Adding some style

If a component needs any custom styling not already provided
by Capital Framework or cfgov-refresh,
you can it by creating a new Less file for the component.

If you're working on a general-purpose atomic component for site-wide use,
this file should live in `cfgov/unprocessed/css/<atoms|molecules|organisms>/`.
(Choose the deepest folder according to the atomic rank of the component.)
Continuing the `RelatedContent` example, if it needed its own styles,
it would live at `cfgov/unprocessed/css/molecules/related-content.less`.

Newly-created Less files need to be imported into the project's master
`main.less` file, located at `cfgov/unprocessed/css/main.less`.
Please place them in the appropriate section for their atomic rank.

Because cfgov-refresh uses `main.less` to build a single CSS file
for almost the entire project, it is not necessary
to tell the Python model anything about a component-specific stylesheet
(for general-purpose, site-wide components).
That is _not_ the case with JavaScript, as we will see in the next section.

!!! note
    If you're working on a component that belongs to a particular sub-app,
    its Less file should live in `cfgov/unprocessed/<app-name>/css/`,
    but how those Less files get built and included on their pages is
    not something this document is prepared to discuss at the moment.

#### Adding some JavaScript

Each atomic component may optionally be given a `Media` class that can
list one or more JavaScript files that should be loaded when using it.
When a page is requested via the browser,
[code contained in `base.html`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/jinja2/v1/_layouts/base.html#L100-L110)
will loop all atomic components for the requested page and
load the appropriate atomic JavaScript bundles.

Here is how one would add the `Media` class to our `RelatedContent` example:

```python
class RelatedContent(blocks.StructBlock):
    …  # see first example on this page

    class Media:
        js = ['related-content.js']
```

(The `related-content.js` file would need to be placed in
`cfgov/unprocessed/js/molecules/`.)

This will load the `related-content.js` script on any page
that includes the `RelatedContent` molecule in one of its StreamFields.




## How-to guides


### Adding a field

1. Locate the Python class of the component you want to add a field to.
1. Add the field by inserting a snippet like this in the list of fields,
   in the order in which you want it to appear in the editor:
   `field_name = blocks.BlockName()`.
   - Replace `field_name` with a succinct name for what data the field contains
   - Replace `BlockName` with one of the
     [basic Wagtail block types](https://docs.wagtail.io/en/v1.13.4/topics/streamfield.html#basic-block-types).
     Sometimes we create our own custom blocks that can be used, as well.
     See, for example, the
     [`HeadingBlock`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/blocks.py#L147-L165),
     [used in `InfoUnitGroup`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/atomic_elements/organisms.py#L54),
     among other places.
1. Add any desired parameters:
   - `required=False` if you do _not_ want the field to be required
     (it usually is, by default)
   - `label='Some label'` if you would like the editor to show a label more
     meaningful than the sentence-case transformation of the field name
   - `help_text='Some text'` if the field needs a more verbose explanation to
     be shown in the editor to make it clear to users how it should work
   - `default=<some appropriate value>` if you want the field to have a
     specific default value, e.g., `True` to have a `BooleanBlock` checkbox
     default to checked.
   - Certain blocks may take other arguments, as described in the
     [basic Wagtail blocks documentation](https://docs.wagtail.io/en/v1.13.4/topics/streamfield.html#basic-block-types).
1. [Edit the component template](#the-html-template) to do something with the
   field's data – output it, use it to trigger a CSS class, etc.
1. [Create a schema migration.](#creating-migrations-for-streamfield-blocks)


### Editing a field

1. [Determine if the change you want to make will need a data migration.](#you-may-also-need-a-data-migration)
   - If the answer is **no**: make your changes,
     [create a schema migration](#creating-migrations-for-streamfield-blocks), and be on your merry way.
   - If the answer is **yes**: continue on.
1. [Add the new version of the field.](#adding-a-field)
1. [Create a schema migration](#creating-migrations-for-streamfield-blocks) for adding the new field.
1. [Create a data migration](#you-may-also-need-a-data-migration)
   to copy data from the old field into the new field.
1. [Edit the component template](#the-html-template)
   to use the new field's data instead of the old field's data.
1. [Remove the old field.](#removing-a-field)
1. [Create a schema migration](#creating-migrations-for-streamfield-blocks) for removing the old field.


### Removing a field

These instructions presume that you do not care
about any data stored in the field you are deleting.
If that is not the case, please go up to the
[instructions for editing a field](#editing-a-field)
and come back here when instructed.

1. Locate the field you want to remove in the block's Python class.
1. Delete the field definition.
1. [Create a schema migration.](#creating-migrations-for-streamfield-blocks)


### Creating migrations for StreamField blocks

To automatically generate a **schema migration**, run
`./cfgov/manage.py makemigrations -n <description_of_changes>`
from the root of the repository.

#### You may also need a data migration

Some field edits (like changing the `default`, `label`, `help_text`,
and `required` properties, or changing the order of fields on a block)
do not require a data migration. A schema migration is sufficient.

However, if you…

- … are renaming an existing field …
- … are deleting a field (or converting it to a new type of field)
  and don't want to lose any existing data stored in that field …
- … are renaming a block within a page's StreamField definition …
- … are deleting a block (or converting it to a new type of block)
  and don't want to lose any existing data stored in that field …

… then you will need a data migration!

In other words, if an existing field is changing,
any data stored in that field has to be migrated to the new field,
unless you're OK with jettisoning it.

---

For more details on both kinds of migrations,
see [the Wagtail Migrations page](../wagtail-migrations/).
