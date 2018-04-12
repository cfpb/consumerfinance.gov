# Notes on Atomic Design

Check out [Don't Build Pages, Build Modules](https://www.ebaytechblog.com/?p=3113).
It encompasses exactly what we are trying to achieve by building components
using atomic design.
It's important to note that our front-end atomic architecture is still evolving.

Our components are broken down into templates, organisms, molecules, and atoms.
We opted not to use the page component, although it exists in atomic design.
Our components are composed of HTML, CSS, and JS (JavaScript).
If a component doesn’t have user interactions or require styling,
then it won’t have an associated JS and/or CSS file.

We compose our atomic components as follows:

### Atoms

Prefixed with “a-” in CSS, JavaScript, and HTML files.

#### HTML

```html
<div class="a-overlay u-hidden"></div>
```

#### CSS

```css
 .a-overlay {
    // Only show overlay at mobile/tablet size.
    .respond-to-max( @bp-sm-max, {
        height: 100%;
        width: 100%;
 …
```


### Molecules ###

Prefixed with “m-” in CSS, JavaScript, and HTML files.

#### HTML

```html
<div class="m-notification
            m-notification__visible
            m-notification__error"
     data-js-hook="state_atomic_init">
    <span class="m-notification_icon cf-icon"></span>
    <div class="m-notification_content" role="alert">
        <div class="h4 m-notification_message">Page not found.</div>
    </div>
</div>
```

#### CSS

```css
.m-notification {
    display: none;
    position: relative;
    padding: @notification-padding__px;
    …
```

#### JavaScript

```javascript
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
```

The notification molecule can be instantiated with the following code:

```javascript
const notification = new Notification( _dom );
notification.init();
```

### Organisms

Prefixed with “o-” in CSS, JavaScript, and HTML.

#### HTML

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

JavaScript:

```javascript
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
```

The Expandable organism can be instantiated with the following code:

```javascript
const expandable = new Expandable( _dom.querySelector( '.o-expandable' ) );
expandable.init( _expandable.EXPANDED );
```

or

```javascript
const atomicHelpers = require( '../../modules/util/atomic-helpers' );
const Expandable = require( '../../organisms/Expandable' );
atomicHelpers.instantiateAll( '.o-expandable', Expandable );
```

### Templates

Prefixed with “t-” in CSS, JavaScript, and HTML. [View all available templates](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/jinja2/v1) that can be extended or reused to create pages.

#### CSS
```css
.t-careers {
    &_social .m-social-media {
        float: right;
    }
    …
```

### Folder structure

Our atomic components are separated and named based on asset type. HTML, CSS, and JavaScript for each component are in separate directories.

#### Current structure

#### HTML
```
cfgov-refresh/cfgov/jinja2/v1/_includes/atoms/
cfgov-refresh/cfgov/jinja2/v1/_includes/molecules/
cfgov-refresh/cfgov/jinja2/v1/_includes/organisms/
```

#### CSS

```
cfgov-refresh/cfgov/unprocessed/css/atoms/
cfgov-refresh/cfgov/unprocessed/css/molecules/
cfgov-refresh/cfgov/unprocessed/css/organisms/
```

#### JavaScript

```
cfgov-refresh/cfgov/unprocessed/js/atoms/
cfgov-refresh/cfgov/unprocessed/js/molecules/
cfgov-refresh/cfgov/unprocessed/js/organisms/
```

#### Test

```
cfgov-refresh/test/unit_tests/atoms/
cfgov-refresh/test/unit_tests/molecules/
cfgov-refresh/test/unit_tests/organisms/
```

### JavaScript architecture

JavaScript components are built to be rendered on the server and then enhanced via JavaScript on the client. The basic interface for the components is as follows:

```javascript
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

#### Articles

[A Simple Challenge to Classical Inheritance Fans](https://medium.com/javascript-scene/a-simple-challenge-to-classical-inheritance-fans-e78c2cf5eead#.mtrvhcjiw)
[Composition over Inheritance (Youtube)](https://www.youtube.com/watch?v=wfMtDGfHWpA)


## Component build pipeline

#### Gulp

Gulp is used as a task automation tool. Tasks include compiling CSS, creating a standard webpack workflow for bundling scripts, minifying code, linting, image optimizing, running unit tests, and [more](https://github.com/cfpb/cfgov-refresh/tree/master/gulp).

#### Webpack

Wepback is used as a module bundler although it's capable of more.
We create page, global, and atomic specific bundles.
The configuration for the bundles is contained in config/webpack-config.js.
An explanation for the usage of each bundle is contained in scripts.js.

#### Routes

Routes are used to serve JavaScript bundles to the browser based
on the requested URL or Wagtail page Media property.
This happens via code contained in [base.html](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/jinja2/v1/_layouts/base.html#L236-L285). This file serves as the base HTML template for serving up assets and content. [View base.html on Github](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/jinja2/v1/_layouts/base.html).

#### Wagtail page media property

Each atomic component has a media property that list the JavaScript files
that should be rendered via base.html.
When a page is requested via the browser, code contained in base.html will
loop all atomic components for the requested page and render
the appropriate atomic JavaScript bundles.

Here is an example of the media property on a component from the [Email signup organism](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/atomic_elements/organisms.py#L223-L224):

```
class Media:
    js = ['email-signup.js']
```

This will load the `email-signup.js` script on any page that includes the Email Signup organism in its template.
