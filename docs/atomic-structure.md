# Notes on Atomic Design

In general, our components employ the concept of atomic design,
meaning that we break them down into atoms, molecules, and organisms,
each successive level being more complex than the previous.
(We do not currently use the template or page concepts as described in
[Brad Frost's seminal article introducing atomic design](http://bradfrost.com/blog/post/atomic-web-design/)).

Our components are composed (on the front-end) of HTML, SCSS (Sass), and JavaScript.
If a component doesn’t have user interactions or require styling,
then it won’t have an associated JS and/or SCSS file.

## CSS class name prefixes

The atomic components have CSS class names with the prefixes `a-`, `m-`, `o-`,
corresponding to atoms, molecules, and organisms. Additionally, utility classes
have the `u-` prefix. These classes are for one-off adjustments, that are shared
across several components and don't fit neatly into the atomic hierarchy.

## Folder structure

Our atomic components are separated and named based on asset type.
HTML, SCSS, and JavaScript for each component are in separate directories.

### HTML

```
consumerfinance.gov/cfgov/v1/jinja2/v1/includes/atoms/
consumerfinance.gov/cfgov/v1/jinja2/v1/includes/molecules/
consumerfinance.gov/cfgov/v1/jinja2/v1/includes/organisms/
```

!!! note

    Some of our foundational components get their SCSS and JavaScript
    from the [Design System](https://cfpb.github.io/design-system/),
    but the HTML for their Wagtail block templates
    is stored in the above folders.

### CSS

```
consumerfinance.gov/cfgov/unprocessed/css/atoms/
consumerfinance.gov/cfgov/unprocessed/css/molecules/
consumerfinance.gov/cfgov/unprocessed/css/organisms/
```

### JavaScript

```
consumerfinance.gov/cfgov/unprocessed/js/molecules/
consumerfinance.gov/cfgov/unprocessed/js/organisms/
```

### Tests

```
consumerfinance.gov/test/unit_tests/js/molecules/
consumerfinance.gov/test/unit_tests/js/organisms/
```

## JavaScript architecture

JavaScript components are built to be rendered on the server
and then enhanced via JavaScript on the client.

We generally favor composition over inheritance.
You can get more information by reading the following:

- [A Simple Challenge to Classical Inheritance Fans](https://medium.com/javascript-scene/a-simple-challenge-to-classical-inheritance-fans-e78c2cf5eead#.mtrvhcjiw)
- [Composition over Inheritance (YouTube)](https://www.youtube.com/watch?v=wfMtDGfHWpA)

## Component build pipeline

### Routes

Routes are used to serve JavaScript bundles to the browser based
on the requested URL or Wagtail page's `Media` definition.
This happens via code contained in
[`v1/layouts/base.html`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/jinja2/v1/layouts/base.html#L85-L123). This file serves as the base HTML template for serving Wagtail pages.

### Wagtail page `Media` class

Each atomic component has a `Media` class that lists the JavaScript files
that should be loaded via `base.html`.
When a page is requested via the browser, code contained in `base.html` will
loop all atomic components for the requested page and load
the appropriate atomic JavaScript bundles.

Here is an example of the `Media` class on a component,
[the `EmailSignUp` organism](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/atomic_elements/organisms.py#L223-L244):

```python
class Media:
    js = ['email-signup.js']
```

This will load the `email-signup.js` script on any page
that includes the `EmailSignUp` organism in one of its StreamFields.
