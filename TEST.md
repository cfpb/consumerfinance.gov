# Browser Tests

## Quick start:

_Note: If you haven’t, make sure to install Protractor globally with `npm install protractor@2.1.0 -g`._

__Update Selenium Server binaries:__

```sh
webdriver-manager update
```

__Start Selenium Server:__

```sh
webdriver-manager start
```

__Open a new tab and cd to the test directory, then tell protractor to start the tests:__

```sh
cd test/browser_tests
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

## Running MacroPolo Tests

From within the `/test/macro_tests/` directory:

1. Install the requirements: `pip install -r requirements.txt`.
2. Run the test runner: `python test_macros.py`.

## Writing Tests

Please see [Macro Polo](https://github.com/cfpb/macropolo) for
documentation about writing tests.


# Content Processor Tests

Test the Sheer content processors that bring content into Elasticsearch
for cfgov-refresh.

## Running

From within the `/test/processor_tests/` directory:

1. Install the requirements: `pip install -r requirements.txt`.
2. Run the test runner: `python test_processors.py`.

## Writing

Tests are written using Python's [`unittest`](https://docs.python.org/2/library/unittest.html) (`unittest2` in Python 2.6).

The tests use JSON files to mock HTTP request's (`request.get()`) response content.

An example:

```python
class WordpressPostProcessorTestCase(unittest.TestCase):
    @mock.patch('requests.get')
    def test_post(self, mock_requests_get):
        mock_response = mock.Mock()
        mock_response.content = open(os.path.join(os.path.dirname(__file__),
                                    'test_wordpress_post_processor_post.json')).read()
        mock_requests_get.return_value = mock_response

        name = 'post'
        url = 'http://mockmockmock/api/get_posts/'

        documents = list(wordpress_post_processor.documents(name, url))

        # ... make assertions about resulting document ...
```
