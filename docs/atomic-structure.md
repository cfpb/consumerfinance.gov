# Notes on Atomic Design

Our components employ the concept of atomic design, meaning that
we break them down into atoms, molecules, and organisms,
each successive level being more complex than the previous.
(We do not currently use the template or page concepts as described in
[Brad Frost's seminal article introducing atomic design](http://bradfrost.com/blog/post/atomic-web-design/)).

Our components are composed (on the front-end) of HTML, Less, and JavaScript.
If a component doesn’t have user interactions or require styling,
then it won’t have an associated JS and/or Less file.
Components that are available for adding to a Wagtail page also
require some Python programming—see the
[creating and editing components](../editing-components/) page for details.

We compose our atomic components as follows:


## Atoms

The smallest kind of component.
May not contain any other components.
Prefixed with `a-` in class names.

### HTML

```html
<div class="a-tag">
    Tag label {{ svg_icon('error') }}
</div>
```

### Less

```css
.a-tag {
    cursor: default;
    display: inline-block;
    padding: 5px 10px;
    …
}
```

### JavaScript

None of our atoms require any JavaScript at this time.


## Molecules

The medium-sized component.
May contain atoms.
Prefixed with `m-` in class names.

### HTML

```html
<div class="m-notification
            m-notification__visible
            m-notification__error"
     data-js-hook="state_atomic_init">
    {{ svg_icon('error') }}
    <div class="m-notification_content" role="alert">
        <div class="h4 m-notification_message">Page not found.</div>
    </div>
</div>
```

### Less

```css
.m-notification {
    display: none;
    position: relative;
    padding: @notification-padding__px;
    …
}
```

### JavaScript

```js
function Notification( element ) {
  const BASE_CLASS = 'm-notification';

  // Constants for the state of this Notification.
  const SUCCESS = 'success';
  const WARNING = 'warning';
  const ERROR = 'error';

  // Constants for the Notification modifiers.
  const MODIFIER_VISIBLE = BASE_CLASS + '__visible';
  const _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  const _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  …
}
```

The Notification molecule can be instantiated
by adding the following to your project's JavaScript code:

```js
const notification = new Notification( _dom );
notification.init();
```


## Organisms

The largest component.
May contain atoms, molecules, or
(if no other solution is viable) other organisms.
Prefixed with `o-` in class names.

### HTML

```html
<div class="o-expandable
            o-expandable__borders
            o-expandable__midtone
            o-expandable__expanded"
     data-js-hook="state_atomic_init">
    <button class="o-expandable_target" aria-pressed="true">
        <div class="o-expandable_header">
        …
```

### Less

```css
.o-expandable {
    position: relative;

    &_target {
        padding: 0;
        border: 0;
        …
    }
    …
}
```

### JavaScript

```js
 function Expandable( element ) {
  const BASE_CLASS = 'o-expandable';

  // Bitwise flags for the state of this Expandable.
  const COLLAPSED = 0;
  const COLLAPSING = 1;
  const EXPANDING = 2;
  const EXPANDED = 3;

  // The Expandable element will directly be the Expandable
  // when used in an ExpandableGroup, otherwise it can be the parent container.
  const _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  const _target = _dom.querySelector( '.' + BASE_CLASS + '_target' );
  const _content = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  …
}
```

The Expandable organism can be instantiated
by adding the following to your project's JavaScript code:

```js
const expandable = new Expandable( _dom.querySelector( '.o-expandable' ) );
expandable.init( _expandable.EXPANDED );
```

or

```js
const atomicHelpers = require( '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js' );
const Expandable = require( '../../organisms/Expandable' );
atomicHelpers.instantiateAll( '.o-expandable', Expandable );
```


## Folder structure

Our atomic components are separated and named based on asset type.
HTML, Less, and JavaScript for each component are in separate directories.

### HTML

```
consumerfinance.gov/cfgov/jinja2/v1/_includes/atoms/
consumerfinance.gov/cfgov/jinja2/v1/_includes/molecules/
consumerfinance.gov/cfgov/jinja2/v1/_includes/organisms/
```

!!! note
    Some of our foundational components get their Less and JavaScript
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
The basic interface for the components is as follows:

```js
function AtomicComponent( domElement ) {
    // Ensure the passed in Element is in the DOM.
    // Query and store references to sub-elements.
    // Instantiate child atomic components.
    // Bind necessary events for referenced DOM elements.
    // Perform other initialization related tasks.
    this.init = function init(){}

    // General teardown function
    // We don't remove the element from the DOM so
    // we need to unbind the events.
    this.destroy = function destroy(){}
}
```

We generally favor composition over inheritance.
You can get more information by reading the following:

- [A Simple Challenge to Classical Inheritance Fans](https://medium.com/javascript-scene/a-simple-challenge-to-classical-inheritance-fans-e78c2cf5eead#.mtrvhcjiw)
- [Composition over Inheritance (YouTube)](https://www.youtube.com/watch?v=wfMtDGfHWpA)


## Component build pipeline

### Gulp

Gulp is used as a task automation tool.
Tasks include compiling CSS, creating a standard Webpack workflow for bundling
scripts, minifying code, linting, running unit tests,
and [more](https://github.com/cfpb/consumerfinance.gov/tree/main/gulp).

### Webpack

Wepback is used as a module bundler, although it's capable of more.
We create page, global, and component-specific bundles.
The configuration for the bundles is contained in
[`config/webpack-config.js`](https://github.com/cfpb/consumerfinance.gov/blob/main/config/webpack-config.js).
An explanation for the usage of each bundle is contained in
[`gulp/tasks/scripts.js`](https://github.com/cfpb/consumerfinance.gov/blob/main/gulp/tasks/scripts.js).

### Routes

Routes are used to serve JavaScript bundles to the browser based
on the requested URL or Wagtail page's `Media` definition.
This happens via code contained in
[`base.html`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/jinja2/v1/_layouts/base.html#L85-L123). This file serves as the base HTML template for serving Wagtail pages.

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
