# Wagtail pages

[Wagtail pages](http://docs.wagtail.io/en/v1.13.4/topics/pages.html) are 
[Django models](https://docs.djangoproject.com/en/1.11/topics/db/models/) 
that are constructed of 
[fields](#fields), [StreamFields](#streamfields), and [panels](#panels) 
that are rendered in a standard way. 
All CFPB Wagtail pages should inherit from the 
[`v1.models.base.CFGOVPage` class](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/base.py#L60).

There are types of information defined on a new Wagtail page model: 
basic [database fields](#fields) (like any Django model), 
specialized database fields called [StreamFields](#streamfields) that allow for freeform page content, 
and [editor panels](#panels) that present these fields to content editors. 

## Fields

Database fields in Wagtail pages work exactly the same as in 
[Django models](https://docs.djangoproject.com/en/1.11/topics/db/models/#fields), 
and Wagtail pages can use any [Django model field](https://docs.djangoproject.com/en/1.11/ref/models/fields/). 

For example, our 
[`BrowsePage` includes a standard Django `BooleanField`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/browse_page.py#L54) 
that allows content editors to toggle secondary navigation sibling pages:

```python
from django.db import models

from v1.models.base import CFGOVPage


class BrowsePage(CFGOVPage):
    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)
```

## StreamFields

StreamFields are special Django model fields provided by Wagtail for 
[freeform page content](https://docs.wagtail.io/en/v1.13.4/topics/streamfield.html). 
They allow a content editor to pick any number number of optional components
and place them in any order within their StreamField. 
In practice this provides the 
[flexibilty of a large rich text box with the structure of individual components](https://torchbox.com/blog/rich-text-fields-and-faster-horses/).

For example, our [`LandingPage` page model includes a `header` StreamField](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/landing_page.py#L13) that can have a hero and/or a text introduction:

```python
from wagtail.wagtailcore.fields import StreamField

from v1.atomic_elements import molecules
from v1.models import CFGOVPage


class LandingPage(CFGOVPage):

    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)
```

**Insert link to StreamField docs here.**

## Panels

Editor panels define how the page's [fields](#fields) and [StreamFields](#streamfields) will be organized for content editors.

The base Wagtail `Page` class and the [`v1.models.base.CFGOVPage` class](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/base.py#L60) 
defines a specific set of panels to which all fields should be added:

- `content_panels`. 
  These fields appear on the "General Content" tab when editing a page. 
  For page body content.
- [`sidefoot_panels`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/base.py#L114-L116).
  These fields appear on the "Sidebar" tab when editing a page. 
- [`settings_panels`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/base.py#L118-L125).
  Appears on the "Configuration" tab when editing a page. 
  Page configuration such as the categories, tags, scheduled publishing, etc.

Most fields will simply require a `FieldPanel` to be added to one of the sets of panels above. 
StreamFields will require a `StreamFieldPanel`. 
See the [Wagtail documentation for additional, more complex panel options](https://docs.wagtail.io/en/v1.13.4/topics/pages.html#editor-panels).

For example, in our `BrowsePage` (used in the [database fields example above](#fields),
[the `secondary_nav_exclude_sibling_pages` `BooleanField` is added to the `sidefoot_panels` as a `FieldPanel`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/browse_page.py#L63):

```python
from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from v1.models.base import CFGOVPage


class BrowsePage(CFGOVPage):
    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # …

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]
```

In out `LandingPage` (used in the [StreamFields example above](#streamfields), 
[the `header` StreamField is added to the `content_panels` as a `StreamFieldPanel`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/landing_page.py#L31):

```python
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField

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

Wagtail provides two attributes to page models that enable restricting the types of subpages or parent pages a particular page model can have. 

For example, in our [interactive regulations page models](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/regulations3k/models/pages.py#L138) 
we have a `RegulationLandingPage` that can be created anywhere in the page tree. 
`RegulationLandingPage`, however, can only have two types of pages created within it: 
`RegulationPage` and `RegulationSearchPage`. 
This parent/child relationship is expressed by setting `subpage_types` on `RegulationLandingPage`
and `parent_page_types` on `RegulationPage` and `RegulationSearchPage` 
to either the model classes themselves or to a model name in the form `app_label.ModelName`:

```python
from v1.models import CFGOVPage


class RegulationLandingPage(CFGOVPage):
    subpage_types = ['regulations3k.RegulationPage', 'RegulationsSearchPage']


class RegulationsSearchPage(CFGOVPage):
    parent_page_types = ['regulations3k.RegulationLandingPage']
    subpage_types = []


class RegulationPage(CFGOVPage):
    parent_page_types = ['regulations3k.RegulationLandingPage']
    subpage_types = []
```

!!! note 
    Note: by setting `subpage_types` to an empty list on `RegulationPage` and `RegulationSearchPage`, 
    we ensure that neither of these pages can have child pages.

## Template rendering

Sometimes new Wagtail page types will need to make customizations to their base template when rendering the page.
This is done by overriding the `template` attribute on the page model.

For example, the [interactive regulations landing page](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/regulations3k/models/pages.py#L138) 
includes a customized list of recently issued notices that gets loaded dynamically from the Federal Register. 
To do this it provides its own template that inherits from our base templates 
and overrides the `content_sidebar` block to include a seperate `recent_notices` template:

```python
from v1.models import CFGOVPage


class RegulationLandingPage(CFGOVPage):
    template = 'regulations3k/landing-page.html'
```

And [`regulations3k/landing-page.html`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/regulations3k/jinja2/regulations3k/landing-page.html#L5):

```jinja2
{% extends 'layout-2-1-bleedbar.html' %}

{% import 'recent-notices.html' as recent_notices with context %}

{% block content_sidebar scoped -%}
    {{ recent_notices }}
{%- endblock %}

{% block javascript scoped %}
    {{ super() }}
    <script async>
      if ( document.body.parentElement.className.indexOf( 'no-js' ) === -1 ) {
        !function(){
          {# Include site-wide JavaScript. #}
          var s = [
            '{{ static('apps/regulations3k/js/index.js') }}',
            '{{ static('apps/regulations3k/js/recent-notices.js') }}'
          ];
          jsl(s);
        }()
      }
    </script>
{% endblock javascript %}
```
