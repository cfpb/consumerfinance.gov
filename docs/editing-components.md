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
   1. [The Python class](#the-python-class)
   1. [Adding it to a StreamField](#adding-it-to-a-streamfield)
   1. [The HTML template](#the-html-template)
   1. [Adding some style](#adding-some-style)
   1. [Adding some JavaScript](#adding-some-javascript)
1. [How-to guides](#how-to-guides)
   1. [Adding, editing, or removing fields in the Wagtail editor](#adding-editing-or-removing-fields)
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


### The Python class

A component's fields and other properties are defined in a Python class file
corresponding to the level of the component.

These files—`atoms.py`, `molecules.py`, and `organisms.py`—are located in
[`cfgov/v1/atomic_elements`](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements).

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
2. The `heading` block uses the basic Wagtail `CharBlock`, which results in a
   field with a basic single-line text input.
3. The `paragraph` block uses the basic Wagtail `RichTextBlock`,
   which results in a field with a multiline WYSIWYG text input.
4. The `links` block uses another basic Wagtail block, `ListBlock`,
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


### Adding it to a StreamField

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

!!! note "Warning: Migrations may be required!"
    Changes to either of the Python bits will usually require
    a new schema migration file, and _may_ require a data migration.
    See
    ["Creating migrations for StreamField blocks"](#creating-migrations-for-streamfield-blocks)
    below.

With the Python pieces covered, it's time to talk about the front end.
First: the markup.


### The HTML template

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
it includes the values of its sub-blocks in an object named `value`.
Above, you can see where the sub-blocks are output with
[Jinja2 expression tags](http://jinja.pocoo.org/docs/2.10/templates/#expressions).
In particular, note how the `links` `ListBlock` is iterated over,
and the values of _its_ `Hyperlink` child blocks are output.

That's about as simple an example as it gets, but block templates can get much
more complex when they have lots of child blocks and grandchild blocks.


### Adding some style

If a component needs any custom styling not already provided
by Capital Framework or cfgov-refresh,
you can it by creating a new Less file for the component.
This file should live in `cfgov/unprocessed/css/<atoms|molecules|organisms>`.
Choose the deepest folder according to the atomic rank of the component.
Continuing the `RelatedContent` example, if it needed its own styles,
it would live at `cfgov/unprocessed/css/molecules/related-content.less`.

Newly-created Less files need to be imported into the project's master
`main.less` file, located at `cfgov/unprocessed/css/main.less`.
Please place them in the appropriate section for their atomic rank.

Because cfgov-refresh uses `main.less` to build a single CSS file
for the entire project, it is not necessary
to tell the Python model anything about a component-specific stylesheet.
That is _not_ the case with JavaScript, as we will see in the next section.


### Adding some JavaScript

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


### Adding, editing, or removing fields

#### Adding a field

1. Locate the Python class of the component you want to add a field to in
   [atoms.py](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements/atoms.py),
   [molecules.py](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements/molecules.py),
   or [organisms.py](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements/organisms.py).
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
1. [Create a schema migration.](#schema-migrations)

#### Removing a field

These instructions presume that you do not care
about any data stored in the field you are deleting.
If that is not the case, please skip to the
[instructions for editing a field](#editing-a-field)
and come back here when instructed.

1. Locate the field you want to remove in the block's Python class, either in
   [atoms.py](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements/atoms.py),
   [molecules.py](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements/molecules.py),
   or [organisms.py](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/v1/atomic_elements/organisms.py).
1. Delete the field definition.
1. [Create a schema migration.](#schema-migrations)

#### Editing a field

1. [Determine if the change you want to make will need a data migration.](#you-may-also-need-a-data-migration)
   - If the answer is **no**: make your changes,
     [create a schema migration](#schema-migrations), and be on your merry way.
   - If the answer is **yes**: continue on.
1. [Add the new version of the field.](#adding-a-field)
1. [Create a schema migration](#schema-migrations) for adding the new field.
1. [Create a data migration](../wagtail-migrations/)
   to copy data from the old field into the new field.
1. [Edit the component template](#the-html-template)
   to use the new field's data instead of the old field's data.
1. [Remove the old field.](#removing-a-field)
1. [Create a schema migration](#schema-migrations) for removing the old field.


### Creating migrations for StreamField blocks

**tl;dr:**

1. `./cfgov/manage.py makemigrations -n <description_of_changes>`
1. [Determine if a data migration is needed](#you-may-also-need-a-data-migration)

#### Schema migrations

Any time you edit a Python file related to a component,
it's a good idea to check and see whether or not you need to include
a schema migration file in your changes, and sometimes also a data migration.

To see if a schema migration is required, run the following command
from the root of the cfgov-refresh repository,
within your local Docker or virtualenv environment:

```bash
./cfgov/manage.py makemigrations --dry-run
```

If anything shows up, you need a schema migration.
Run the following, editing it to give your migration a name
that briefly describes the change(s) you're making:

```bash
./cfgov/manage.py makemigrations -n <description_of_changes>
```

Include the created file (located in `cfgov/v1/migrations/`)
in your pull request along with the other changes.

#### You may also need a data migration

Some field edits (like changing the `default`, `label`, `help_text`,
and `required` properties, or changing the order of fields on a block)
do not require a data migration. A schema migration is sufficient.

However, if you…

- … are renaming an existing field …
- … are deleting a field (or converting it to a new type of field)
  and don't want to lose any existing data stored in that field …
- … are renaming a block within a StreamField definition …
- … are deleting a block (or converting it to a new type of block)
  and don't want to lose any existing data stored in that field …

… then you will need a data migration!

In other words, if an existing field is changing,
any data stored in that field has to be carefully migrated to the new field,
unless you're OK with jettisoning it.

**Data migrations are not easy.**
There is no automatic generation mechanism like there is for schema migration.
You must write the script by hand that automates the transfer of data
from old fields to new fields.

As described in the "Editing a component" how-to above,
it's a three-step process to modify a field without losing data:

1. Create the new field with an automatic schema migration
2. Use a handwritten data migration script to move data
   from the old field to the new field
3. Delete the old field with an automatic schema migration

We're getting out of scope for this document, though.
For more details, please visit
the [Wagtail Migrations](../wagtail-migrations/) page,
or consult your friendly local back-end developer.
