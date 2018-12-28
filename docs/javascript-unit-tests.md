# Writing tests

This page provides instructions for writing a new JavaScript unit test in cfgov-refresh.

For documentation on *running* tests, see [https://cfpb.github.io/cfgov-refresh/testing-fe/#unit-testing](https://cfpb.github.io/cfgov-refresh/testing-fe/#unit-testing)


## Setting up tests

[Jest](https://jestjs.io/docs/en/getting-started) is the framework we use for writing and running JavaScript unit tests.

We recommend using Test-Driven Development (TDD) when you are coding new JavaScript. This requires you to set up your test at the same time as your new JavaScript, so that you write your test first, with the expected behavior and functionality well-described, **then** you write the code that makes the test pass. A [better summary is](http://www.javiersaldana.com/tech/2014/11/26/refactoring-the-three-laws-of-tdd.html):

> 1.  Write only enough of a unit test to fail.
> 2.  Write only enough production code to make the failing unit test pass.


[Read this primer on Test-Driven Development](https://medium.freecodecamp.org/test-driven-development-what-it-is-and-what-it-is-not-41fa6bca02a2?gi=3c8d8b476cc9) to learn about how it differs from the typical approach to programming and unit tests.

### New test file from sample

For this guide, we'll use very basic sample code files to illustrate how to use the test framework in cfgov-refresh and how to test very common code patterns.

Another common approach is to look for existing tests that are testing something similar to what you are writing now. Feel free to do so and sub another test file for the `sample-spec.js` file referenced below. For links to existing tests, see the [Running tests](#running-tests) section on this page.

Now, let's begin! Let's make a new unit test fail, then we will make it pass, following the principles of TDD.

1. Create 2 new files: a test file, and a JavaScript file. Their names should match, with the test file adding a `-spec.js` suffix. For example, if your script is named `my-javascript.js`, then your test is named `my-javascript-spec.js`.
1. Copy the code from this [`sample-spec.js` file](https://github.com/cfpb/cfgov-refresh/blob/fc9ecc002f933a432322bd15f54be5eb2cffa6e3/test/unit_tests/js/modules/sample-spec.js) into your own test file.
1. Copy and paste from [`sample.js`](https://github.com/cfpb/cfgov-refresh/blob/fc9ecc002f933a432322bd15f54be5eb2cffa6e3/cfgov/unprocessed/js/modules/sample.js) into your new JavaScript file.

### Folder structure (where to put your JavaScript and tests)

JavaScript unit test files belong in the [cfgov-refresh/test/unit_tests/](https://github.com/cfpb/cfgov-refresh/tree/master/test/unit_tests) directory.

The folder structure of the test files mirrors the structure of the project JavaScript in [cfgov-refresh/cfgov/unprocessed/js/](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/unprocessed/js).

So my `sample-spec.js` file is in `test/unit_tests/modules` and my `sample.js` file is in `cfgov/unprocessed/js/modules` . I put these files in the `modules` folder because they are not atomic components, they are just sample files. Your JavaScript might be an atomic element, in which case, it should go in the corresponding folder. If you're not sure where your JavaScript should go, [read about atomic components in cfgov-refresh](/atomic-structure/).

---

!!! note "Child apps"
    If you’re working on something in a child app, put it in `test/unit_test/appname/js/`. Otherwise, if you’re working on something that belongs to cfgov-refresh generally, it should go in the corresponding folder under `test/unit_test/js/`.


Now that you have your sample JS and test files in the right places, let’s try running them and see what happens! I'll refer to `sample-spec.js` and `sample.js` in the instructions below, but you should work in your own new test file and JavaScript file to save and commit your changes.

1. Edit line 7 of your spec file and remove the `.skip` method. The line should now read: 
    ```
    it( 'should return a string with expected value', () => {
    ```

1. Run your sample test using `gulp test:unit --specs=js/modules/sample-spec.js` (subbing with your own filename). The test should fail- this is expected. Remember, when doing TDD, we want to write our test to fail first, then write the corresponding JavaScript that will make the test pass.
1. Make the test pass by changing your script's line 7 (see [`sample.js`](https://github.com/cfpb/cfgov-refresh/blob/fc9ecc002f933a432322bd15f54be5eb2cffa6e3/cfgov/unprocessed/js/modules/sample.js)) to the following:
    ```
    return ‘Shredder’;
    ```
1. Run the test again to confirm the test now passes. Doesn’t it feel good?

[Jump to the "Running Tests" section of this page](#running-tests) for additional commands to run tests.

### File structure (basic layout of a test file)

In order to make the `sample-spec.js` more meaningful to your own use case, you’ll need to know how to structure a unit test using Jest methods. Let’s take a look at the structure of our very basic sample test file.

#### Imports

Line 1 of any spec file will use `import` statements to include the JavaScript file that you are testing. Additional dependencies should be added in the same manner.

```
import * as sample from '../../../../cfgov/unprocessed/js/modules/sample.js';
```

Some test files use `const` declarations to require scripts instead of `import`, because those files were written before `import` was available. We prefer to use `import` because it allows [tree shaking in Webpack](https://webpack.js.org/guides/tree-shaking/), meaning if two modules are importing the same module it should only be included in the bundle once, whereas with `require` it would be included twice.

A consequence is that variables can't be used in the import path, since it breaks Webpack figuring out which modules are duplicates. For example, this code should be converted to an `import` statement, but without including the `BASE_JS_PATH` variable in the file path:

```
const FooterButton = require( BASE_JS_PATH + 'modules/footer-button.js' ) // works but could duplicate other required files
import * as FooterButton from BASE_JS_PATH + 'modules/footer-button.js' // doesn't work and the build will fail
import * as FooterButton from '../../../../cfgov/unprocessed/js/modules/footer-button.js' // is ugly but it works, has tree shaking

```

Imports also provide a benefit in that you can import specific parts of a module so that you only import the dependencies you need. For testing purposes, we will typically import the whole module to make sure we have full test coverage. Read the [`import` reference guide on MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) on how to implement `import` for different use cases.


#### Setup and teardown

Jest has methods for setting up test data, or performing other actions that are needed before and after running a unit test, such as [`beforeEach` and `afterEach`](https://jestjs.io/docs/en/setup-teardown#repeating-setup-for-many-tests), or [`beforeAll` and `afterAll`](https://jestjs.io/docs/en/setup-teardown#one-time-setup).

For example, a common structure when the DOM is involved is to create a constant for an HTML snippet to test, then set that snippet to the document.body in a `beforeEach` before all the tests. See ["Testing DOM manipulation"](#testing-dom-manipulation) in the “Common test patterns” section of this page.

[Check out the Jest documentation on "Setup and teardown" methods](https://jestjs.io/docs/en/setup-teardown).

#### Providing test data

ways to provide data for your tests to operate on


- declare values as variables, for example in this [strings-spec.js]() unit test.
- declare data for each unit test or for several tests using `beforeEach`/`beforeAll`
- 
- HTML markup. For an example of test data that consists of HTML markup, see ["Testing DOM manipulation"](#testing-dom-manipulation) in the “Common test patterns” section of this page.



#### Describe() method

The `describe` method is where we put the name of the JavaScript file we are testing. For the sample, this is "sample."

    - root `describe`,
    - child `describe`s

#### Assertions

    - `it` scenarios
    - [`expect` assertions](https://jestjs.io/docs/en/expect#expectvalue)
    - Other types of assertions
- Linter settings that can be ignored in tests
    - Lint warning for over 55 lines: you can ignore this for the root `describe` fn

### Providing test data

- Keep test data as simple as possible – use the minimum needed to test the code

### Spies, stubs, and mocks

- Sinon-y stuff – spies, stubs, and mocks – when do you use each? how to do with Jest?

### Error handling

What did we mean by this?


## Common test patterns

### Testing a basic function

Testing simple functions is pretty straightforward.
Each function in a module should have tests set up as
a child `describe` within the module’s own `describe`.
Then, write a number of `it` statements in prose that describe
how the function should respond to various kinds of input.
Inside each `it`, invoke the function
with the input described in the `it` statement
and use `expect` to check that you receive the desired result.

Here is a simple example from our
[array helpers module](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/unprocessed/js/modules/util/array-helpers.js)
(`cfgov/unprocessed/js/modules/util/array-helpers.js`):

```js
function indexOfObject( array, key, val ) {
  let match = -1;

  if ( !array.length > 0 ) {
    return match;
  }

  array.forEach( function( item, index ) {
    if ( item[key] === val ) {
      match = index;
    }
  } );

  return match;
}
```

Tests for that function, from
[test/unit_tests/js/modules/util/array-helpers-spec.js](https://github.com/cfpb/cfgov-refresh/blob/master/test/unit_tests/js/modules/util/array-helpers-spec.js):

```js
describe( 'indexOfObject()', () => {
  it( 'should return -1 if the array is empty', () => {
    array = [];
    index = arrayHelpers.indexOfObject( array, 'foo' );

    expect( index ).toBe( -1 );
  } );

  it( 'should return -1 if there is no match', () => {
    array = [
      { value: 'bar' },
      { value: 'baz' }
    ];
    index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

    expect( index ).toBe( -1 );
  } );

  it( 'should return the matched index', () => {
    array = [
      { value: 'foo' },
      { value: 'bar' },
      { value: 'baz' }
    ];
    index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

    expect( index ).toBe( 0 );
  } );
} );
```

### Testing DOM manipulation

[Jest](https://jestjs.io/en/), the JavaScript testing framework we use,
[includes jsdom](https://jestjs.io/docs/en/configuration#testenvironment-string),
which simulates a DOM environment as if you were in the browser.
This means that we can call any
[DOM API](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)
in our test code and observe it in the same way as we do
in the module code itself, which acts on the browser’s DOM.

As an example, let’s look at our Notification component.
The Notification component uses a common set of markup
with different classes and SVG icon code to style it
as a particular kind of notification (success, warning, etc.). In
[the component JS](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/unprocessed/js/molecules/Notification.js),
we have this function that sets the type of a notification before displaying it:

```js
function _setType( type ) {
  // If type hasn't changed, return.
  if ( _currentType === type ) {
    return this;
  }

  // Remove existing type class
  const classList = _dom.classList;
  classList.remove( BASE_CLASS + '__' + _currentType );


  if ( type === SUCCESS ||
       type === WARNING ||
       type === ERROR ) {
    // Add new type class and update the value of _currentType
    classList.add( BASE_CLASS + '__' + type );
    _currentType = type;

    // Replace <svg> element with contents of type_ICON
    const currentIcon = _dom.querySelector( '.cf-icon-svg' );
    const newIconSetup = document.createElement( 'div' );
    newIconSetup.innerHTML = ICON[type];
    const newIcon = newIconSetup.firstChild;
    _dom.replaceChild( newIcon, currentIcon );
  } else {
    throw new Error( type + ' is not a supported notification type!' );
  }
  return this;
}
```

This function would be invoked by an instance of the Notification class.
`_dom` is the DOM node for the Notification.
As you can see from the code comments above,
it has a few different steps that modify the DOM node.

Now let’s look at the tests.
Here are the first 22 lines of
[the spec file](https://github.com/cfpb/cfgov-refresh/blob/master/test/unit_tests/js/molecules/Notification-spec.js)
that tests this component:

```js
import Notification from '../../../../cfgov/unprocessed/js/molecules/Notification';
const BASE_CLASS = 'm-notification';
const HTML_SNIPPET = `
  <div class="m-notification
              m-notification__default">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"></svg>
    <div class="m-notification_content">
      <div class="h4 m-notification_message">Notification content</div>
    </div>
  </div>
`;

describe( 'Notification', () => {
  let notificationElem;
  let notification;
  let thisNotification;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    notificationElem = document.querySelector( `.${ BASE_CLASS }` );
    notification = new Notification( notificationElem, BASE_CLASS, {} );
  } );

  …
} );
```

The main things to note here at the beginning of the file are
the addition of the `HTML_SNIPPET` definition,
containing the markup we will used for testing
as it would be rendered for this component,
and the `beforeEach` function that
(1) uses jsdom to add that snippet to the test environment
and assigns the component node to the `notificationElem` variable, and
(2) creates a new instance of the Notification class.

!!! A word about `HTML_SNIPPET`s
    Right now it's possible to update a component’s Jinja template,
    forget to update the corresponding JavaScript,
    and the unit tests would still pass,
    because they're using their own `HTML_SNIPPET`.
    It would be preferable if we had a canonical component markup template
    that is pulled in by the application, the unit tests, and the docs.
    We haven’t yet figured out how to do this, since
    our component templates contain Jinja tags that
    the tests would have to reconcile
    into a complete, finished chunk of markup.
    For now, just be aware of this when
    [editing a Wagtail component that includes JavaScript](../editing-components/).

Further down, here are some of the tests that cover the `_setType` function
(by way of the `setTypeAndContent` function that
wraps both `_setType` and `_setContent`):

```js
describe( 'setTypeAndContent()', () => {
  it( 'should update the notification type for the success state', () => {
    notification.init();

    notification.setTypeAndContent(
      notification.SUCCESS,
      ''
    );

    expect( notificationElem.classList ).toContain( 'm-notification__success' );
  } );

  it( 'should update the notification type for the warning state', () => {
    notification.init();

    notification.setTypeAndContent(
      notification.WARNING,
      ''
    );

    expect( notificationElem.classList ).toContain( 'm-notification__warning' );
  } );

  …
} );
```

This part mostly works like testing any other function.
The notable distinction here is that the test invokes the function
using the DOM nodes and class set up in `beforeEach`.

### Testing browser state

Another common thing to test is code that interacts with
the state of the browser itself,
e.g., fragment identifiers, query strings, or other things in the URL;
the window object; session storage; page history; etc.

One way of doing this is to create a **spy**
(a special kind of mocked function)
that watches for browser API calls to be made
a certain number of times or with a specific payload.
One example is found in
[the tests for our full-table-row-linking code](https://github.com/cfpb/cfgov-refresh/blob/master/test/unit_tests/js/modules/o-table-row-links-spec.js).

In
[the module code](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/unprocessed/js/modules/o-table-row-links.js)
(`o-table-row-links.js`),
if an event listener detects a click anywhere on
one of these special table rows,
it invokes `window.location` to send the browser
to the `href` of the first link in that row:

```js
window.location.assign( target.querySelector( 'a' ).getAttribute( 'href' ) );
```

To test this, in the aforementioned `o-table-row-links-spec.js` file, we first
[set up a standard Jest mock](https://jestjs.io/docs/en/mock-functions)
for `window.location.assign`, and then
[create our spy](https://jestjs.io/docs/en/jest-object#jestspyonobject-methodname)
to watch it:

```js
describe( 'o-table-row-links', () => {
  beforeEach( () => {
    window.location.assign = jest.fn();
    locationSpy = jest.spyOn( window.location, 'assign' );
    …
  } );

  …
} );
```

A little further down (after finishing the DOM setup
and initializing the module we’re testing),
we have three tests that simulate clicks
and then assert things that the spy can answer for us:
whether it was called with a particular location parameter,
and that it was called a specific number of times (zero).

```js
it( 'should navigate to new location when link row cell clicked', () => {
  simulateEvent( 'click', linkRowCellDom );
  expect( locationSpy ).toBeCalledWith( 'https://www.example.com' );
} );

it( 'should not set window location when link is clicked', () => {
  simulateEvent( 'click', linkDom );
  expect( locationSpy ).toHaveBeenCalledTimes( 0 );
} );

it( 'should not navigate to new location when non link row cell clicked',
  () => {
    simulateEvent( 'click', nonLinkRowCellDom );
    expect( locationSpy ).toHaveBeenCalledTimes( 0 );
  }
);
```

### Testing user interaction

Testing user interaction with simulated pointer events, keystrokes,
or form submissions is best handled via browser tests, not unit tests.
User interaction in a unit test could falsely pass
if the component wasn't visible on the page, for instance.
[Read more about how we run browser tests.](../browser-tests/)

## Running tests

TBA!