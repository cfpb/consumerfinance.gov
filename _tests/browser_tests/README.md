## Quick start:

_Note: If you haven't, make sure to install Protractor globally with `npm install protractor@2.1.0 -g`._

__Update Selenium Server binaries:__

```sh
webdriver-manager update
```

__Start Selenium Server:__

```sh
webdriver-manager start
```

__Open a new tab and cd to this directory, then tell protractor to start the tests:__

```sh
protractor conf.js
```

If you want to test a server other than your local instance (assuming port 7000 is your local CFGov server) use the `--baseUrl` flag. Ex:

```sh
protractor conf.js --baseUrl=http://beta.consumerfinance.gov
# or
protractor conf.js --baseUrl=http://localhost:8000
```

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

Tests are organized into suites. Common tests are in the `/shared` directory and any non-standard test should be added to an existing additional suite or placed into a new suite directory. An example shared suite for our the-bureau example page above would be:

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

Protractor was created by the Angular team to do end-to-end testing of angular sites. It extends the selenium api and makes certain allowences for angularjs. To make it work correctly with non-angular sites you MUST include the following bit of code in your conf.js file.

```js
  beforeEach(function() {
    return browser.ignoreSynchronization = true;
  });
```

Enjoy! :relieved:
