# Browser Tests

## Quick start:

Open a new Terminal window or tab and change to the project directory,
then tell gulp to start the tests:

```sh
gulp build
gulp test:acceptance
```

If you want to test a server other than your local instance,
edit the `HTTP_HOST` and `HTTP_PORT` values in your `.env` file
and reload the settings with `cd .. && cd cfgov-refresh`. Type `y` if prompted.

## Sauce Connect - send tests to the cloud

Sauce Labs can be used to run tests remotely in the cloud.

1. Log into [http://saucelabs.com/account](Log into http://saucelabs.com/account).
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
   > Note: If you want to temporarily disable testing on Sauce Labs,
   run the command as: `gulp test:acceptance --sauce=false`.
8. Monitor progress of the tests
   on the [Sauce Labs dashboard](https://saucelabs.com/dashboard) Automated Tests tab.

> Note: If you get the error `Error: ENOTFOUND getaddrinfo ENOTFOUND`
  while running a test, it likely means that Sauce Connect is not running.
  See step 4 above.

## Manual test configuration

A number of command-line arguments can be set to test particular configurations:

 - `--specs`: Choose a particular spec suite to run.
   For example, `gulp test:acceptance --specs=contact-us.js`.
   Multiple tests can be run by passing in a comma-separated list of test suite filenames.
   For example, `gulp test:acceptance --specs=contact-us.js,about-us.js`.
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

## Pages

Pages are organized in `page_objects`. To add new tests start with adding a new page file and include the elements you'll want to query the page for. For example, if you wanted to test the page title and all the `h2` elements on the about page you'd write:

```js
function TheBureauPage() {
  this.get = function() {
    // Always use the relative url because the baseUrl is set for us
    browser.get( '/the-bureau/' );
  };

  // Page titles are available to the browser global
  this.pageTitle = function() { return browser.getTitle() };
  // We want all the `bureau-mission_section` so we'll use .all()
  this.missions = element.all( by.css( '.bureau-mission_section h1' ) );
  // For a list of all locators see http://angular.github.io/protractor/#/api?view=webdriver.By
}

module.exports = TheBureauPage;
```

## Tests

Tests are organized into suites. Common tests are in the `test/browser_tests/spec_suites/shared` directory and any non-standard test should be added to an existing additional suite or placed into a new suite directory. An example shared suite for our the-bureau example page above would be:

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

## Further Reading

- [Protractor](http://angular.github.io/protractor/#/)
- [Select elements on a page](http://www.seleniumhq.org/docs/03_webdriver.jsp#locating-ui-elements-webelements)
- [Writing Jasmin expectations](http://jasmine.github.io/2.0/introduction.html#section-Expectations).
- [Understanding Page Objects](http://www.thoughtworks.com/insights/blog/using-page-objects-overcome-protractors-shortcomings)

## Important note:

Protractor was created by the Angular team to do end-to-end testing of angular sites. It extends the Selenium API and makes certain allowences for AngularJS. To make it work correctly with non-Angular sites you MUST include the following bit of code in your conf.js file.

```js
  beforeEach(function() {
    return browser.ignoreSynchronization = true;
  });
```

Enjoy! :relieved:


# Template Macro Tests

Test the Jinja2 templates. From within the root project directory run `gulp test:unit:macro`.

## Writing Tests

Please see [Macro Polo](https://github.com/cfpb/macropolo) for
documentation about writing tests.

# Performance Testing

To audit if the site complies with performance best practices and guidelines,
run `gulp test:perf`.

The audit will run against [sitespeed.io performance rules](https://www.sitespeed.io/rules/)
and crawl the website from the homepage.
You can adjust the settings to skip rules and change the crawling depth
by editing `/gulp/tasks/test.js`.

# Django Server Unit Tests

To run the server unit tests using Tox,
make sure the `TOXENV` variable is set in your `.env` file and
run `gulp test:unit:server` from the command-line in the project root.


# Accessibility Testing

To audit a page's WCAG and Section 508 accessibility:
  1. Enable the environment variable `ACHECKER_ID` in your `.env` file.
     Get a free [AChecker API ID](http://achecker.ca/register.php) for the value.
  2. Reload your `.env` with `. ./.env` while in the project root directory.
  3. Run `gulp test:a11y` to run an audit on the homepage.
  4. To test a page aside from the homepage, add the `--u=<path_to_test>` flag.
     For example, `gulp test:a11y --u=contact-us`
     or `gulp test:a11y --u=the-bureau/bureau-structure/`.
