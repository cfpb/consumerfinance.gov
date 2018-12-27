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
- Common Test Patterns
    - Testing a simple function
    - Testing DOM manipulation
        - Jsdom incorporated into Jest
    - Testing user interaction / events
- Running Tests
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

I’ve decided to put my sample-test.js file in cfgov/unprocessed/js/**modules** because ____???__. So my sample-test-spec.js file will go in test/unit_tests/**modules**.

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