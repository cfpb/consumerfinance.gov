# Notes on Atomic Design

Check out [Don't Build Pages, Build Modules](http://www.ebaytechblog.com/?p=3113). It encompasses exactly what we are trying to achieve by building components using atomic design. It's important to note that our front-end atomic architecture is still evolving.

Our components are broken down into templates, organisms, molecules, and atoms. We opted not to use the page component, although it exists in atomic design. Our components are composed of HTML, CSS, and JavaScript. If a component doesn’t have user interactions or require styling, then it won’t have an associated js and/or css file. We compose our atomic components as follows:

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
```


### Molecules ###

Prefixed with “m-” in CSS, JavaScript, and HTML files.

#### HTML

```html
<div class="m-notification m-notification__error m-notification__visible" data-js-hook="state_atomic_init">
      <span class="m-notification_icon cf-icon"></span>
      <div class="m-notification_content" role="alert"></div>
 </div>
```

#### CSS

```css
.m-notification {
    display: none;
    position: relative;
    padding: @m-notification-padding__px;
    padding-left: 40px;
```

#### JavaScript

```javascript
function Notification( element ) { 
   // eslint-disable-line max-statements, inline-comments, max-len
   var BASE_CLASS = 'm-notification';

   // Constants for the state of this Notification.
   var SUCCESS = 'success';
   var WARNING = 'warning';
   var ERROR = 'error'; 
   // Constants for the Notification modifiers.
   var MODIFIER_VISIBLE = BASE_CLASS + '__visible'; 
   var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
   var _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );
```

The notification molecule can be instantiated with the following code:

```javascript
_notification = new Notification( _dom );
_notification.init();
```

### Organisms

Prefixed with “o-” in CSS, JavaScript, and HTML.

#### HTML

```html
<div data-qa-hook="expandable" class="o-expandable 
                                      o-expandable__borders 
                                      o-expandable__midtone 
                                      o-expandable__expanded" 
                               data-js-hook="state_atomic_init">
    <button class="o-expandable_target" aria-pressed="true">
        <div class="o-expandable_header">
```

JavaScript:

```javascript
 function Expandable( element ) { 
  var BASE_CLASS = 'o-expandable';

  // Bitwise flags for the state of this Expandable.
  var COLLAPSED = 0;
  var COLLAPSING = 1;
  var EXPANDING = 2;
  var EXPANDED = 3;

  // The Expandable element will directly be the Expandable
  // when used in an ExpandableGroup, otherwise it can be the parent container.
  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _target = _dom.querySelector( '.' + BASE_CLASS + '_target' );
  var _content = _dom.querySelector( '.' + BASE_CLASS + '_content' );
```
  
The Expandable organism can be instantiated with the following code:

```javascript
_expandable = new Expandable( _dom.querySelector( '.o-expandable' ) );
_expandable.init( _expandable.EXPANDED );
```

or

```javascript
var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var Expandable = require( '../../organisms/Expandable' );
atomicHelpers.instantiateAll( '.o-expandable', Expandable );
```

### Templates

Prefixed with “t-” in CSS, JavaScript, and HTML.

#### CSS
```css
.t-careers {
    &_social .m-social-media {
        float: right;
    }

    // TODO: Consolidate site-wide media_image responsive sizes into one class.
    &_students-and-graduates .media_image {
        width: 130px;
        .respond-to-min( @bp-med-min, {
            width: 150px;
        } );
```

### Folder Structure

Atomic code is currently separated and named based on asset type. This is a mistake in my view, as I believe we should begin migrating to a modular folder structure based on the component.

#### Current Structure

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

#### Proposed Folder Structure

```
cfgov-refresh/cfgov/front-end/molecules/Expandable

Expandable.html
Expandable.css
Expandable.js
Expandable-unit-test.js
README.MD
```

### JavaScript Architecture

There was considerable discussion on how we should create JS components. The components aren't constructed to be used on SPAs (Single Page Applications). They are built to be rendered on the sever and then enhanced via JavaScript on the client. The basic interface for the components is as follows:

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

We aren't testing for interface adherence but we probably should. We generally favor composition over inheritance. You can get more information by reading the following:

#### Articles

[A Simple Challenge to Classical Inheritance Fans](https://medium.com/javascript-scene/a-simple-challenge-to-classical-inheritance-fans-e78c2cf5eead#.mtrvhcjiw)
[Composition over Inheritance (Youtube)](https://www.youtube.com/watch?v=wfMtDGfHWpA)

#### Code and Related PRs

[View Unit Test](https://github.com/cfpb/cfgov-refresh/pull/916)
[Expandable example 1](http://jsfiddle.net/0j9u66h0/9/)
[Expandable example 2](https://jsfiddle.net/cpsyLy3L/2/)

## Component Build Pipeline

#### Gulp

Gulp is used as a task automation tool. A specific breakdown of each task is contained [here](https://github.com/cfpb/cfgov-refresh#available-gulp-tasks).

#### Webpack

Wepback is used as a module bundler although it's capable of more. We create page, global, and atomic specific bundles. The configuration for the bundles is contained in webpack-config.js. An explanation for the usage of each bundle is contained in scripts.js.

#### Routes

Routes are used to serve JavaScript bundles to the browser based on the requested URL or Wagtail page Media property. The happens via code contained in base.html.

#### Base.html

This file serves as the base document for serving up assets and content. It's currently very complicated, obtrusive, and needs to be refactored.

#### Wagtail Page Media Property

Each Atomic component has a media property which list the JavaScript files that should be rendered via base.html. When a page is requested via the browser, code contained in base.html will loop all Atomic components for the requested page and render the appropriate Atomic JavaScript bundles.

#### Questions and Concerns

- How do we support Single Page Applications and be functional when JavaScript is disabled?
- How do we ensure creation of performant atomic components?
- Is the codebase lacking uniformity?
- CSS bloat when multiple components are on the same page but from different Django apps.
- Ensuring simplicity over complexity.
