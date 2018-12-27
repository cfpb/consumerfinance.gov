# Writing JavaScript unit tests

This page provides instructions for writing a new JavaScript unit test in cfgov-refresh.

For documentation on *running* tests: [https://cfpb.github.io/cfgov-refresh/testing-fe/#unit-testing](https://cfpb.github.io/cfgov-refresh/testing-fe/#unit-testing)


## Table of contents

- Setting up tests
    - New File from sample
    - Folder structure (where to put it)
    - File structure (basic layout of a test file)
    - Providing test data
    - Spies, stubs, and mocks
    - Error handling
- Common test patterns
    - Testing a basic function
    - Testing DOM manipulation
    - Testing browser state
    - Testing user interaction
- Running tests
    - Commands/fit in existing documentation on how to run tests in diff environments (locally, Travis, Jenks, etc)
    - link to existing tests
    - Test coverage
        - Only shows coverage for unit tests and not acceptance tests
        - What is our expected level of test coverage for unit tests?
        - Are there certain scripts we want to exclude from test coverage because they are covered or should be covered by acceptance tests?
    - how to read test coverage output, how we test coverage, etc.
- Other sources of information
    - Jest docs
    - Istanbul docs
    - JSDom docs


## Setting up tests

Context: we use Jest, we use (BDD) assertion style

Jest is the framework we use for writing and running JavaScript unit tests.

### New test file from sample

We recommend using Test-Driven Development (TDD) when you are coding new JavaScript. This requires you to set up your test at the same time as your new JavaScript, so that you write your test first, with the expected behavior and functionality well-described, **then** you write the code that makes the test pass.

Note: a common approach is to look for existing tests that are testing something similar to what you are writing now. Feel free to do so and sub another test file for the sample-test-spec.js file referenced below. For links to existing tests, see the [Running tests](#Running-tests) section on this page.


1. Add new test file, named after your JavaScript file. So if you are adding tests for my-javascript.js, create a new file named my-javascript-spec.js
1. Copy this sample-test-spec.js file:
1. [Todo: Add sample to cfgov-refresh and run it] this is in progress at [https://github.com/cfpb/cfgov-refresh/compare/add-sample-js-unit-test?expand=1](https://github.com/cfpb/cfgov-refresh/compare/add-sample-js-unit-test?expand=1)
1. And this sample-test.js file: [link or paste code here]

### Folder structure (where to put your JavaScript and tests)

JavaScript unit test files belong in the [cfgov-refresh/test/unit_tests/](https://github.com/cfpb/cfgov-refresh/tree/master/test/unit_tests) directory.

The folder structure of the test files mirrors the structure of the project JavaScript in [cfgov-refresh/cfgov/unprocessed/js/](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/unprocessed/js).

For example, if you’re working on something in a child app, put it in test/unit_test/appname/js/…, and if you’re working on something that belongs to cfgov-refresh generally, it should go in the corresponding folder under test/unit_test/js/.

I’ve decided to put my sample-test.js file in cfgov/unprocessed/js/**modules** because __???__. So my sample-test-spec.js file will go in test/unit_tests/**modules**.

Now that you have your sample JS and test files in the right places, let’s try running them and see what happens!

- Edit line 7 of sample-test-spec.js and remove the ".skip" method. The line should now read “it(‘should return a string’), ( )
- Run your sample test using `gulp test:unit --specs=js/modules/sample-test-spec.js`. The test should fail- this is expected. When doing TDD, we want to write our test to fail first, then write the corresponding JavaScript that will make the test pass.
- Make the test pass by changing your sample-test.js line 7 to the following:
    - return ‘Shredder’;
- Run `gulp test:unit --specs=js/modules/sample-test-spec.js` again to confirm the test now passes. Doesn’t it feel good?

[Jump to the "Running Tests" section of this page](#heading=h.902hhlo4mqzw) for additional commands to run tests.

### File structure (basic layout of a test file)

In order to make the sample-test-spec.js more meaningful to your own use case, you’ll need to know how to structure a unit test using Jest methods. Let’s take a look at the structure of our very basic sample test file.

#### Imports

Line 1

- Import and const
#### Test data and markup

#### Setup and teardown

Jest has methods for setting up test data, or performing other actions that are needed before and after running a unit test, such as [`beforeEach` and `afterEach`](https://jestjs.io/docs/en/setup-teardown#repeating-setup-for-many-tests), or [`beforeAll` and `afterAll`](https://jestjs.io/docs/en/setup-teardown#one-time-setup).

For example, a common structure when the DOM is involved is to create a constant for an HTML snippet to test, then set that snippet to the document.body in a `beforeEach` before all the tests. See "Testing DOM manipulation" in the “Common test patterns” section of this page.

[Check out the Jest documentation on "Setup and teardown" methods](https://jestjs.io/docs/en/setup-teardown).

#### Describe() method

The `describe` method is where we put the name of the JavaScript file we are testing. For the sample, this is "sample-test."

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
