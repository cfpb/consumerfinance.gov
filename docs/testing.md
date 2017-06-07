# Browser tests

## Quick start:

Many of our browser tests have been rewritten as Python unit tests. The remaining rely on data that is not generated during testing, so please note many of these tests might fail if you do not have a production database locally. If you do, open a new Terminal window or tab and change to the project directory,
then tell gulp to start the tests:

```sh
gulp build
gulp test:acceptance --suite=integration
gulp test:acceptance --suite=content

```

If you want to test a server other than your local instance,
edit the `HTTP_HOST` and `HTTP_PORT` values in your `.env` file
and reload the settings with `cd .. && cd cfgov-refresh`. Type `y` if prompted.

## Sauce Connect - send tests to the cloud

!!! danger
    The instruction for automatically
    running Sauce Connect from gulp are not working.
    See https://github.com/cfpb/cfgov-refresh/issues/2324

Sauce Labs can be used to run tests remotely in the cloud.

1. Log into [http://saucelabs.com/account](http://saucelabs.com/account).

2. [Download Sauce Connect](https://docs.saucelabs.com/reference/sauce-connect/#basic-setup)

3. Open a new Terminal window or tab and navigate to the downloaded SauceConnect folder.
    If you place the folder in your Application's folder this might look like:

    ```
    cd /Users/<YOUR MAC OSX USERNAME>/Applications/SauceConnect
    ```

4. Copy step 3 from the the SauceLabs
   [Basic Setup instructions](https://wiki.saucelabs.com/display/DOCS/Basic+Sauce+Connect+Setup#BasicSauceConnectSetup-SettingUpSauceConnect)
   and run that in your Terminal window.
   Once you see `Sauce Connect is up` in the Terminal,
   that means the tunnel has successfully been established

    > The Terminal command should already have your Sauce username and access key filled in.
      If it doesn't, make sure you're logged in.

5. Update and uncomment the `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY`,
   and `SAUCE_SELENIUM_URL` values in your `.env` file.
   The access key can be found in lower-left on the Sauce Labs
   [account profile page](https://saucelabs.com/account/profile).

6. Reload the settings with `cd .. && cd cfgov-refresh`. Type `y` if prompted.

7. Run the tests with `gulp test:acceptance`.

    !!! Note:
        If you want to temporarily disable testing on Sauce Labs,
        run the command as: `gulp test:acceptance --sauce=false`.

8. Monitor progress of the tests
   on the [Sauce Labs dashboard](https://saucelabs.com/dashboard) Automated Tests tab.

!!! Note
    If you get the error `Error: ENOTFOUND getaddrinfo ENOTFOUND`
    while running a test, it likely means that Sauce Connect is not running.
    See step 4 above.

## Manual test configuration

A number of command-line arguments can be set to test particular configurations:

 - `--suite`: Choose a particular suite or suites to run.
   For example, `gulp test:acceptance --suite=content` or `gulp test:acceptance --suite=content,functional`.
 - `--specs`: Choose a particular spec or specs to run.
   For example, `gulp test:acceptance --specs=contact-us.js`, `gulp test:acceptance --specs=contact-us.js,about-us.js`, or `gulp test:acceptance --specs=foo*.js`. If `--suite` is specified, this argument will be ignored. If neither `--suite` nor `--specs` are specified, all specs will be run.
 - `--windowSize`: Set the window size in pixels in `w,h` format.
   For example, `gulp test:acceptance --windowSize=900,400`.
 - `--browserName`: Set the browser to run.
   For example, `gulp test:acceptance --browserName=firefox`.
 - `--version`: Set the browser version to run.
   For example, `gulp test:acceptance --version='44.0'`.
 - `--platform`: Set the OS platform to run.
   For example, `gulp test:acceptance --platform='osx 10.10'`.
 - `--sauce`: Whether to run on Sauce Labs or not.
   For example, `gulp test:acceptance --sauce=false`.


## Tests

Tests are organized into suites under the `test/browser_tests/spec_suites/` directory. Any new tests should be added to an existing suite or placed into a new suite directory. An example test for our the-bureau example page above would be:

```js
var TheBureauPage = require( '../../page_objects/page_the-bureau.js' );

describe( 'Beta The Bureau Page', function() {
  var page;

  beforeEach( function() {
    page = new TheBureauPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'The Bureau' );
  } );

  it( 'should include 3 bureau missions titled Educate, Enforce, Empower', function() {
    expect( page.missions.count() ).toEqual( 3 );
    expect( page.missions.getText() ).toEqual[ 'Educate', 'Enforce', 'Empower' ];
  } );
} );
```

## Further reading

- [Protractor](http://angular.github.io/protractor/#/)
- [Select elements on a page](http://www.seleniumhq.org/docs/03_webdriver.jsp#locating-ui-elements-webelements)
- [Writing Jasmin expectations](http://jasmine.github.io/2.0/introduction.html#section-Expectations).
- [Understanding Page Objects](http://www.thoughtworks.com/insights/blog/using-page-objects-overcome-protractors-shortcomings)


# Performance testing

To audit if the site complies with performance best practices and guidelines,
run `gulp test:perf`.

The audit will run against
[Google's PageSpeed Insights](https://github.com/addyosmani/psi).


# Django and Python unit tests

To run the the full suite of Python 2.7 unit tests using Tox, cd to the project
root, make sure the `TOXENV` variable is set in your `.env` file and then run

```
tox
```

If you haven't changed any installed packages and you don't need to test all migrations, you can run a much faster Python code test using:
```
tox -e fast
```

To see Python code coverage information, run
```
./show_coverage.sh
```


# Accessibility Testing

Run the acceptance tests with an `--a11y` flag (i.e. `gulp test:acceptance --a11y`)
to check every webpage for WCAG and Section 508 compliancy using Protractor's
[accessibility plugin](https://github.com/angular/protractor-accessibility-plugin).

If you'd like to audit a specific page, use `gulp test:a11y`:

  1. Enable the environment variable `ACHECKER_ID` in your `.env` file.
     Get a free [AChecker API ID](http://achecker.ca/register.php) for the value.
  2. Reload your `.env` with `source ./.env` while in the project root directory.
  3. Run `gulp test:a11y` to run an audit on the homepage.
  4. To test a page aside from the homepage, add the `--u=<path_to_test>` flag.
     For example, `gulp test:a11y --u=contact-us`
     or `gulp test:a11y --u=the-bureau/bureau-structure/`.

# Source code linting

The default test task includes linting of the JavaScript source, build,
and test files.
Use the `gulp lint` command from the command-line to run the ESLint linter,
which checks the JavaScript against the rules configured in `.eslintrc`.
[See the ESLint docs](http://eslint.org/docs/rules/)
for detailed rule descriptions.

There are a number of options to the command:

 - `gulp lint:build`: Lint only the gulp build scripts.
 - `gulp lint:test`: Lint only the test scripts.
 - `gulp lint:scripts`: Lint only the project source scripts.
 - `--fix`: Add this flag (like `gulp lint --fix` or `gulp lint:build --fix`)
   to auto-fix some errors, where ESLint has support to do so.
