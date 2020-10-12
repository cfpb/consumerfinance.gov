# Wagtail pages

[Wagtail pages](http://docs.wagtail.io/en/stable/topics/pages.html) are 
[Django models](https://docs.djangoproject.com/en/1.11/topics/db/models/) 
that are constructed of 
[fields](#fields), [StreamFields](#streamfields), and [panels](#panels) 
that are rendered in a standard way. 
All CFPB Wagtail pages should inherit from the 
[`v1.models.base.CFGOVPage` class](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/base.py).

!!! note
    Before creating a new Wagtail page type 
    please consider whether one of our existing page types can meet your needs. 
    Talk to the consumerfinance.gov product owners 
    if your content is significantly different from anything else on the site 
    or a specific maintenance efficiency will be gained from a new page type.

There are types of information defined on a new Wagtail page model: 
basic [database fields](#fields) (like any Django model), 
specialized database fields called [StreamFields](#streamfields) that allow for freeform page content, 
and [editor panels](#panels) that present these fields to content editors. 

## Fields

Database fields in Wagtail pages work exactly the same as in 
[Django models](https://docs.djangoproject.com/en/1.11/topics/db/models/#fields), 
and Wagtail pages can use any [Django model field](https://docs.djangoproject.com/en/1.11/ref/models/fields/). 

For example, our `BrowsePage` 
[includes a standard Django `BooleanField`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/browse_page.py) 
that allows content editors to toggle secondary navigation sibling pages:

```python
from django.db import models

from v1.models.base import CFGOVPage


class BrowsePage(CFGOVPage):
    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)
```

## StreamFields

StreamFields are special Django model fields provided by Wagtail for 
[freeform page content](https://docs.wagtail.io/en/stable/topics/streamfield.html). 
They allow a content editor to pick any number number of optional components
and place them in any order within their StreamField. 
In practice, this provides the flexibility of
[a large rich text field, with the structure of individual components](https://torchbox.com/blog/rich-text-fields-and-faster-horses/).

For example, our `LandingPage` page model 
[includes a `header` StreamField](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/landing_page.py) 
that can have a hero and/or a text introduction:

```python
from wagtail.core.fields import StreamField

from v1.atomic_elements import molecules
from v1.models import CFGOVPage


class LandingPage(CFGOVPage):

    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)
```

The specifics of StreamField block components can be found in 
[Creating and Editing Wagtail Components](https://cfpb.github.io/consumerfinance.gov/editing-components/).

## Panels

Editor panels define how the page's [fields](#fields) and [StreamFields](#streamfields) will be organized for content editors;
they correspond to the tabs that appear across the top of the edit view for a page in the Wagtail admin.

The base Wagtail `Page` class and the [`CFGOVPage` subclass of it](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/base.py) 
define specific sets of panels to which all fields should be added:

- `content_panels`:
  For page body content.
  These fields appear on the "General Content" tab when editing a page. 
- `sidefoot_panels`:
  For page sidebar or footer content.
  These fields appear on the "Sidebar" tab when editing a page. 
- `settings_panels`:
  Page configuration such as the categories, tags, scheduled publishing, etc.
  Appears on the "Configuration" tab when editing a page. 

Most fields will simply require a `FieldPanel` to be added to one of the sets of panels above. 
StreamFields will require a `StreamFieldPanel`. 
See the [Wagtail documentation for additional, more complex panel options](https://docs.wagtail.io/en/stable/topics/pages.html#editor-panels).

For example, in our `BrowsePage` (used in the [database fields example above](#fields)),
the `secondary_nav_exclude_sibling_pages` `BooleanField` 
[is added to the `sidefoot_panels` as a `FieldPanel`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/browse_page.py):

```python
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel

from v1.models.base import CFGOVPage


class BrowsePage(CFGOVPage):
    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # …

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]
```

Because `secondary_nav_exclude_sibling_pages` is a boolean field, 
this creates a checkbox on the "Sidebar/Footer" tab when editing a page.
Checking or unchecking that checkbox will set the value of `secondary_nav_exclude_sibling_pages` when the page is saved.

In our `LandingPage` (used in the [StreamFields example above](#streamfields)), 
the `header` StreamField 
[is added to the `content_panels` as a `StreamFieldPanel`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/landing_page.py#L31):

```python
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

from v1.atomic_elements import molecules
from v1.models import CFGOVPage


class LandingPage(CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    # …

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        # …
    ]
```

## Parent / child page relationships

Wagtail provides two attributes to page models that enable 
[restricting the types of subpages or parent pages](https://docs.wagtail.io/en/stable/topics/pages.html#parent-page-subpage-type-rules) 
a particular page model can have. On any page model:

- `parent_page_types` limits which page types this type can be created under.
- `subpage_types` limits which page types can be created under this type.

For example, in our [interactive regulations page models](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/regulations3k/models/pages.py#L138) 
we have a `RegulationLandingPage` that can be created anywhere in the page tree. 
`RegulationLandingPage`, however, can only have two types of pages created within it: 
`RegulationPage` and `RegulationSearchPage`. 
This parent/child relationship is expressed by setting `subpage_types` on `RegulationLandingPage`
and `parent_page_types` on `RegulationPage` and `RegulationSearchPage` 
to a model name in the form 'app_label.ModelName':

```python
from v1.models import CFGOVPage


class RegulationLandingPage(CFGOVPage):
    subpage_types = ['regulations3k.RegulationPage', 'regulations3k.RegulationsSearchPage']


class RegulationsSearchPage(CFGOVPage):
    parent_page_types = ['regulations3k.RegulationLandingPage']
    subpage_types = []


class RegulationPage(CFGOVPage):
    parent_page_types = ['regulations3k.RegulationLandingPage']
    subpage_types = []
```

!!! note 
    We prevent child pages from being added to `RegulationPage` and `RegulationSearchPage` 
    by setting `subpage_types` to an empty list.

## Template rendering

New Wagtail page types will usually need to make customizations to their base template 
[when rendering the page](https://docs.wagtail.io/en/stable/topics/pages.html#template-rendering).
This is done by overriding the `template` attribute on the page model.

For example, the [interactive regulations landing page](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/regulations3k/models/pages.py) 
includes a customized list of recently issued notices that gets loaded dynamically from the Federal Register. 
To do this it provides its own template that inherits from our base templates 
and overrides the `content_sidebar` block to include a separate `recent_notices` template:

```python
from v1.models import CFGOVPage


class RegulationLandingPage(CFGOVPage):
    template = 'regulations3k/landing-page.html'
```

And in [`regulations3k/landing-page.html`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/regulations3k/jinja2/regulations3k/landing-page.html):

```jinja2
{% extends 'layout-2-1-bleedbar.html' %}

{% import 'recent-notices.html' as recent_notices with context %}

{% block content_sidebar scoped -%}
    {{ recent_notices }}
{%- endblock %}
```
